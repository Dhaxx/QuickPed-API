from app.models.pedido import Pedido, PedidoItem, PedidoItemAdicional, StatusPedido
from app.models.produto import Adicional
from app.models.estabelecimento import Estabelecimento
from app.services.base import BaseService
from ..schemas.pedido import PedidoCreate
from sqlmodel import Session, select, update
from sqlalchemy.orm.attributes import flag_modified
from decimal import Decimal
from app.services.produto import Produto
from app.models.comanda import Comanda
from app.models.mesa import Mesa
from app.models.usuario import Usuario
from app.services.impressao import impressao_service
from fastapi import HTTPException, status


class PedidoService(BaseService[Pedido]):
    def create(self, session: Session, estabelecimento_id: int, data: PedidoCreate) -> Pedido:
        estabelecimento = session.get(Estabelecimento, estabelecimento_id)

        if not estabelecimento.esta_aberto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estabelecimento não está aberto",
            )     
        
        itens_processados = []
        total_pedido = Decimal("0.00")

        if not data.nome_cliente or len(data.nome_cliente.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nome do cliente é obrigatório",
            )
        
        numero_mesa = None
        comanda_id = None
        endereco_id = None

        if data.tipo == "Delivery":
            endereco_id = data.endereco_id

            if not endereco_id:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum endereço selecionado para pedido delivery",
                )

        elif data.tipo == "Retirada":
            # Para retirada, não precisa de endereço nem número da mesa
            pass

        elif data.tipo == "Local":
            # Se veio token da mesa, busca por token. Senão, busca por número da mesa
            if data.mesa_token:
                mesa = session.exec(
                    select(Mesa).where(Mesa.token == data.mesa_token, Mesa.ativa == True, Mesa.estabelecimento_id == estabelecimento_id)
                ).one_or_none()

                if not mesa:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="Mesa não encontrada"
                    )
            else:
                mesa = session.exec(
                    select(Mesa).where(
                        Mesa.numero == data.numero_mesa,
                        Mesa.estabelecimento_id == estabelecimento_id,
                        Mesa.ativa == True,
                    )
                ).one_or_none()

                if not mesa:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="Mesa não encontrada"
                    )
            numero_mesa = mesa.numero

            # Verifica se tem comanda aberta com lock (SELECT FOR UPDATE)
            # Isso previne race condition onde duas requisições criam comandas duplicadas
            # Usa nowait=False para esperar caso outra transação já esteja com lock
            comanda = session.exec(
                select(Comanda)
                .where(
                    Comanda.status == "aberta",
                    Comanda.numero_mesa == numero_mesa,
                    Comanda.estabelecimento_id == estabelecimento_id,
                )
                .with_for_update(nowait=False)
            ).one_or_none()

            if not comanda:
                comanda = Comanda(
                    estabelecimento_id=estabelecimento_id,
                    numero_mesa=numero_mesa,
                    status="aberta",
                )
                session.add(comanda)
                session.flush()
                session.refresh(comanda)
            comanda_id = comanda.id

        for item_data in data.itens:
            item = item_data if isinstance(item_data, dict) else item_data.model_dump()

            produto = session.exec(
                select(Produto).where(
                    Produto.id == item.get("produto_id"),
                    Produto.estabelecimento_id == estabelecimento_id,
                )
            ).first()

            if not produto:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Produto {item.get('produto_id')} não encontrado",
                )

            preco_unitario = Decimal(produto.preco)
            quantidade = Decimal(str(item.get("quantidade", 1)))

            if quantidade < 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Quantidade deve ser pelo menos 1",
                )

            subtotal_item = preco_unitario * quantidade

            adicionais = item.get("adicionais", [])
            if adicionais:
                for adicional in adicionais:
                    preco_adicional = (
                        Decimal(adicional.get("preco", 0))
                        if isinstance(adicional, dict)
                        else Decimal(adicional.preco)
                    )
                    subtotal_item += preco_adicional * quantidade

            if produto.produzido_por is not None:
                produtor = session.exec(
                    select(Usuario.usuario).where(Usuario.id == produto.produzido_por)
                ).one_or_none()
            else:
                produtor = None

            item_pedido = PedidoItem(
                produto_id=produto.id,
                nome_produto=produto.nome,
                preco_unitario=preco_unitario,
                quantidade=quantidade,
                adicionais=adicionais,
                produzido_por=produtor,
            )

            itens_processados.append(item_pedido)
            total_pedido += subtotal_item

        itens_json_serializavel = []
        itens_json_sequence = 0

        for i in itens_processados:
            adicionais_serializaveis = []
            for a in i.adicionais:
                # se a veio do banco, deve ter id
                adicionais_serializaveis.append(
                    {
                        "id": getattr(a, "id", None),
                        "nome": a.nome,
                        "preco": float(a.preco),
                    }
                )

            itens_json_sequence += 1

            itens_json_serializavel.append(
                {
                    "item_id": itens_json_sequence,
                    "produto_id": i.produto_id,
                    "nome_produto": i.nome_produto,
                    "preco_unitario": float(i.preco_unitario),
                    "quantidade": i.quantidade,
                    "adicionais": adicionais_serializaveis,
                    "produzido_por": i.produzido_por,
                }
            )

        pedido = Pedido(
            estabelecimento_id=estabelecimento_id,
            comanda_id=comanda_id,
            nome_cliente=data.nome_cliente,
            numero_mesa=numero_mesa,
            itens=itens_json_serializavel,
            total=total_pedido,
            obs=data.obs,
            tipo=data.tipo,
            endereco_id=endereco_id,
        )

        # Update atômico do total da comanda
        # IMPORTANTE: Isso previne race condition onde dois pedidos simultâneos
        # podem sobrescrever o total um do outro ao invés de somar corretamente
        # Sintaxe: UPDATE comanda SET total = total + :valor WHERE id = :id
        if data.tipo == "local":
            comanda_id = comanda.id
            session.exec(
                update(Comanda)
                .where(Comanda.id == comanda_id)
                .values(total=Comanda.total + total_pedido)
            )

        session.add(pedido)
        session.commit()

        # Recarrega o pedido com os dados atualizados do banco
        session.refresh(pedido)

        impressao_service.imprimir_pedido(session, pedido.id, estabelecimento_id)

        return pedido

    def get_by_comanda(
        self, session: Session, mesa_token: str, estabelecimento_id: int
    ) -> list[Pedido]:
        mesa = session.exec(
            select(Mesa).where(
                Mesa.token == mesa_token, Mesa.estabelecimento_id == estabelecimento_id
            )
        ).first()

        if not mesa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Mesa não encontrada"
            )

        comanda = session.exec(
            select(Comanda).where(
                Comanda.numero_mesa == mesa.numero,
                Comanda.estabelecimento_id == estabelecimento_id,
                Comanda.status == "aberta",
            )
        ).first()

        if not comanda:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma comanda aberta para esta mesa",
            )

        return session.exec(
            select(Pedido).where(
                Pedido.comanda_id == comanda.id,
                Pedido.estabelecimento_id == estabelecimento_id,
                Pedido.oculto == False,
            )
        ).all()

    def get_all(self, session: Session, estabelecimento_id: int):
        stmt = select(Pedido).where(
            Pedido.estabelecimento_id == estabelecimento_id,
            Pedido.oculto == False,
        )
        result = session.exec(stmt).all()
        return [
            dict(
                id=p.id,
                nome_cliente=p.nome_cliente,
                numero_mesa=p.numero_mesa,
                obs=p.obs,
                status=p.status.value if hasattr(p.status, "value") else str(p.status),
                total=str(p.total),
                criado_em=p.criado_em.isoformat() if p.criado_em else None,
                itens=p.itens,
                tipo=p.tipo.value if hasattr(p.tipo, "value") else str(p.tipo),
                endereco_id=p.endereco_id,
            )
            for p in result
        ]
    
    def delete_item_pedido(self, session: Session, pedido_id:int, item_id:int, estabelecimento_id: int):
        pedido = session.exec(
            select(Pedido).where(
                Pedido.id == pedido_id,
                Pedido.estabelecimento_id == estabelecimento_id,
                Pedido.oculto == False,
            ).with_for_update(nowait=False)
        ).first()

        if not pedido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado"
            )

        itens = pedido.itens
        item_para_remover = None

        for item in itens:
            if item.get("item_id") == item_id:
                item_para_remover = item
                break

        if not item_para_remover:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item do pedido não encontrado"
            )

        itens.remove(item_para_remover)
        flag_modified(pedido, "itens") # informa ao SQLAlchemy que a lista de itens foi modificada

        # Recalcula o total do pedido
        total_recalculado = Decimal("0.00")
        for i in itens:
            preco_unitario = Decimal(str(i.get("preco_unitario", "0.00")))
            quantidade = Decimal(str(i.get("quantidade", "1")))
            subtotal_item = preco_unitario * quantidade

            adicionais = i.get("adicionais", [])
            if adicionais:
                for adicional in adicionais:
                    preco_adicional = Decimal(str(adicional.get("preco", "0.00")))
                    subtotal_item += preco_adicional * quantidade

            total_recalculado += subtotal_item

        pedido.itens = itens
        pedido.total = total_recalculado

        print(pedido.itens)

        session.add(pedido)
        session.commit()
        session.refresh(pedido)

        return pedido

    def get_pendentes(self, session: Session, estabelecimento_id: int):
        return session.exec(
            select(Pedido).where(
                Pedido.estabelecimento_id == estabelecimento_id,
                Pedido.status == StatusPedido.PENDENTE,
                Pedido.oculto == False,
            )
        ).all()

    def get_para_imprimir(self, session: Session, estabelecimento_id: int):
        return session.exec(
            select(Pedido).where(
                Pedido.estabelecimento_id == estabelecimento_id,
                Pedido.impresso == False,
                Pedido.status not in [StatusPedido.ENTREGUE, StatusPedido.CANCELADO],
                Pedido.oculto == False,
            )
        ).all()

    def marcar_impresso(
        self,
        session: Session,
        pedido_id: int,
        estabelecimento_id: int,
        impresso: bool = True,
    ):
        pedido = session.exec(
            select(Pedido).where(
                Pedido.id == pedido_id,
                Pedido.estabelecimento_id == estabelecimento_id,
                Pedido.oculto == False,
            )
        ).first()
        if pedido:
            pedido.impresso = impresso
            session.add(pedido)
            session.commit()


pedido_service = PedidoService(Pedido)
