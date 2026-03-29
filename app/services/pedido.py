from app.models.pedido import Pedido, PedidoItem, PedidoItemAdicional
from app.models.produto import Adicional
from app.services.base import BaseService
from ..schemas.pedido import PedidoCreate
from sqlmodel import Session, select
from decimal import Decimal
from app.services.produto import Produto
from app.models.comanda import Comanda
from app.models.mesa import Mesa
from app.models.usuario import Usuario
from fastapi import HTTPException, status

class PedidoService(BaseService[Pedido]):
    def create(self, session: Session, estabelecimento_id: int, data: PedidoCreate) -> Pedido:
        itens_processados = []
        total_pedido = Decimal("0.00")

        mesa = session.exec(
            select(Mesa).where(
                Mesa.numero == data.numero_mesa,
                Mesa.estabelecimento_id == estabelecimento_id,
                Mesa.ativa == True
            )
        ).first()

        if not mesa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mesa não encontrada"
            )

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

            if item.adicionais:
                for adicional in item.adicionais:
                    subtotal_item += adicional.preco * item.quantidade

            if produto.produzido_por is not None:
                produtor = session.exec(
                    select(Usuario.usuario).where(Usuario.id == produto.produzido_por)
                ).first()
            else:
                produtor = None

            item_pedido = PedidoItem(
                produto_id=produto.id,
                nome_produto=produto.nome,
                preco_unitario=preco_unitario,
                quantidade=item.quantidade,
                adicionais=item.adicionais,
                produzido_por=produtor
            )

            itens_processados.append(item_pedido)
            total_pedido += subtotal_item

        itens_json_serializavel = []
        for i in itens_processados:
            adicionais_serializaveis = []
            for a in i.adicionais:
                # se a veio do banco, deve ter id
                adicionais_serializaveis.append({
                    "id": getattr(a, "id", None),  # <- aqui você coloca o id
                    "nome": a.nome,
                    "preco": float(a.preco)
                })

            itens_json_serializavel.append({
                "produto_id": i.produto_id,
                "nome_produto": i.nome_produto,
                "preco_unitario": float(i.preco_unitario),
                "quantidade": i.quantidade,
                "adicionais": adicionais_serializaveis,
                "produzido_por": produtor if produtor else None
            })

        if data.mesa_token:
            mesa = session.exec(
                select(Mesa).where(Mesa.token == data.mesa_token, Mesa.ativa == True)
            ).first()
            if not mesa:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Mesa não encontrada"
                )
            numero_mesa = mesa.numero
        else:
            numero_mesa = data.numero_mesa

        pedido = Pedido(
            estabelecimento_id=estabelecimento_id,
            comanda_id=comanda.id,
            nome_cliente=data.nome_cliente,
            numero_mesa=numero_mesa,
            itens=itens_json_serializavel,
            total=total_pedido,
            obs=data.obs
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