from app.models.comanda import Comanda
from app.models.pedido import Pedido
from app.services.base import BaseService
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

class ComandaService(BaseService[Comanda]):
    def recalcular_total(self, session: Session, numero_mesa: int, estabelecimento_id: int):
        comanda = session.exec(
            select(Comanda)
            .where(
                Comanda.numero_mesa == numero_mesa,
                Comanda.estabelecimento_id == estabelecimento_id,
                Comanda.status == 'aberta'
            )
        ).first()
        if not comanda:
            raise ValueError("Comanda não encontrada")
        
        total = session.exec(
            select(Pedido).where(Pedido.comanda_id == comanda.id, Pedido.status != "Cancelado")
        ).all()

        total_comanda = sum(p.total for p in total)
        comanda.total = total_comanda
        session.add(comanda)
        session.commit()
        session.refresh(comanda)
        return

    def get_by_mesa(self, session, numero_mesa: int, estabelecimento_id: int) -> Comanda:
        comanda = session.exec(
            select(Comanda)
            .where(
                Comanda.numero_mesa == numero_mesa,
                Comanda.estabelecimento_id == estabelecimento_id,
                Comanda.status == 'aberta'
            )
            .options(selectinload(Comanda.pedidos))
        ).first()

        if comanda is None:
            raise ValueError("Comanda não encontrada")

        self.recalcular_total(session, numero_mesa, estabelecimento_id)

        return comanda

comanda_service = ComandaService(Comanda)