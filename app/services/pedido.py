from app.models.pedido import Pedido, PedidoItem, PedidoItemAdicional
from app.models.produto import Adicional
from app.services.base import BaseService
from ..schemas.pedido import PedidoCreate
from sqlmodel import Session, select
from decimal import Decimal
from app.services.produto import Produto
from app.models.comanda import Comanda

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

        pedido = Pedido(
            estabelecimento_id=estabelecimento_id,
            comanda_id=comanda.id,
            nome_cliente=data.nome_cliente,
            numero_mesa=data.numero_mesa,
            itens=itens_processados,
            total=total_pedido
        )

        comanda.total += total_pedido
        session.add(comanda)
        session.add(pedido)
        session.commit()
        session.refresh(pedido)

        return pedido
    
pedido_service = PedidoService(Pedido)