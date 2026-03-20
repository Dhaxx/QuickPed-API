from app.models.pedido import Pedido, PedidoItem, PedidoItemAdicional
from app.models.produto import Adicional
from app.services.base import BaseService
from ..schemas.pedido import PedidoCreate
from sqlmodel import Session, select
from decimal import Decimal
from app.services.produto import Produto
from app.models.comanda import Comanda
from app.models.mesa import Mesa
from fastapi import HTTPException, status

class PedidoService(BaseService[Pedido]):
    def create(self, session: Session, estabelecimento_id: int, data: PedidoCreate) -> Pedido:
        itens_processados = []
        total_pedido = Decimal("0.00")

        # Verifica se tem comanda aberta
        comanda = session.exec(
            select(Comanda).where(
                Comanda.status == 'aberta',
                Comanda.numero_mesa == data.numero_mesa,
                Comanda.estabelecimento_id == estabelecimento_id
            )
        ).first()

        if not comanda:
            comanda = Comanda(
                estabelecimento_id=estabelecimento_id,
                numero_mesa=data.numero_mesa,
                status='aberta'
            )
            session.add(comanda)
            session.flush()

        for item in data.itens:
            produto = session.exec(
                select(Produto).where(
                    Produto.id == item.produto_id,
                    Produto.estabelecimento_id == estabelecimento_id
                )
            ).first()

            if not produto:
                raise ValueError(f"Produto {item.produto_id} não encontrado")

            preco_unitario = produto.preco
            subtotal_item = preco_unitario * item.quantidade

            adicionais_processados = []

            if item.adicionais:
                adicionais = session.exec(
                    select(Adicional).where(
                        Adicional.id.in_(item.adicionais),
                        Adicional.estabelecimento_id == estabelecimento_id
                    )
                ).all()

                adicionais_map = {a.id: a for a in adicionais}

                for adicional_id in item.adicionais:
                    adicional = adicionais_map.get(adicional_id)

                    if not adicional:
                        raise ValueError(f"Adicional {adicional_id} inválido")

                    adicionais_processados.append(
                        PedidoItemAdicional(
                            nome=adicional.nome,
                            preco=adicional.preco
                        )
                    )

                    subtotal_item += adicional.preco * item.quantidade

            item_pedido = PedidoItem(
                produto_id=produto.id,
                nome_produto=produto.nome,
                preco_unitario=preco_unitario,
                quantidade=item.quantidade,
                adicionais=adicionais_processados
            )

            itens_processados.append(item_pedido)
            total_pedido += subtotal_item

        itens_json_serializavel = [
            {
                "produto_id": i.produto_id,
                "nome_produto": i.nome_produto,
                "preco_unitario": float(i.preco_unitario),
                "quantidade": i.quantidade,
                "adicionais": [
                    {"nome": a.nome, "preco": float(a.preco)} for a in i.adicionais
                ]
            }
            for i in itens_processados
        ]

        pedido = Pedido(
            estabelecimento_id=estabelecimento_id,
            comanda_id=comanda.id,
            nome_cliente=data.nome_cliente,
            numero_mesa=data.numero_mesa,
            itens=itens_json_serializavel,
            total=total_pedido
        )

        comanda.total += total_pedido
        session.add(comanda)
        session.add(pedido)
        session.commit()
        session.refresh(pedido)

        return pedido
    
    def get_by_comanda(self, session: Session, mesa_token: str, estabelecimento_id: int) -> list[Pedido]:
        mesa = session.exec(
            select(Mesa).where(
                Mesa.token == mesa_token,
                Mesa.estabelecimento_id == estabelecimento_id
            )
        ).first()

        if not mesa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mesa não encontrada"
            )

        comanda = session.exec(
            select(Comanda).where(
                Comanda.numero_mesa == mesa.numero,
                Comanda.estabelecimento_id == estabelecimento_id,
                Comanda.status == 'aberta'
            )
        ).first()

        if not comanda:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma comanda aberta para esta mesa"
            )

        return session.exec(
            select(Pedido).where(
                Pedido.comanda_id == comanda.id,
                Pedido.estabelecimento_id == estabelecimento_id
            )
        ).all()
    
pedido_service = PedidoService(Pedido)