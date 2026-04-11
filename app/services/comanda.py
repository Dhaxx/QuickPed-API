from fastapi import HTTPException
from typing import Optional

from app.models.comanda import Comanda
from app.models.pedido import Pedido
from app.models.mesa import Mesa
from app.services.base import BaseService
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload


class ComandaService(BaseService[Comanda]):
    def get_all(
        self, session: Session, estabelecimento_id: int, status: Optional[str] = None
    ):
        query = select(Comanda).where(
            Comanda.estabelecimento_id == estabelecimento_id,
        )
        if status:
            query = query.where(Comanda.status == status)

        comandas = list(
            session.exec(query.options(selectinload(Comanda.pedidos))).all()
        )

        for comanda in comandas:
            if comanda.status == "aberta":
                self.recalcular_total(session, comanda.numero_mesa, estabelecimento_id)
        return comandas

    def recalcular_total(
        self, session: Session, numero_mesa: int, estabelecimento_id: int
    ):
        # Lock na comanda para evitar race conditions durante o recálculo
        comanda = session.exec(
            select(Comanda)
            .where(
                Comanda.numero_mesa == numero_mesa,
                Comanda.estabelecimento_id == estabelecimento_id,
                Comanda.status == "aberta",
            )
            .with_for_update(nowait=False)
        ).first()
        if not comanda:
            raise HTTPException(status_code=404, detail="Comanda não encontrada")

        # Lock nos pedidos para garantir consistência ao somar totais
        total = session.exec(
            select(Pedido)
            .where(Pedido.comanda_id == comanda.id, Pedido.status != "Cancelado")
            .with_for_update(nowait=False)
        ).all()

        total_comanda = sum(p.total for p in total)
        comanda.total = total_comanda
        session.add(comanda)
        session.commit()
        session.refresh(comanda)
        return

    def get_by_mesa(self, session, token: str) -> Comanda:
        mesa = session.exec(select(Mesa).where(Mesa.token == token)).first()

        comanda = session.exec(
            select(Comanda)
            .where(
                Comanda.numero_mesa == mesa.numero,
                Comanda.estabelecimento_id == mesa.estabelecimento_id,
                Comanda.status == "aberta",
            )
            .options(selectinload(Comanda.pedidos))
        ).first()

        if comanda is None:
            raise HTTPException(status_code=404, detail="Comanda não encontrada")

        self.recalcular_total(session, mesa.numero, mesa.estabelecimento_id)

        return comanda

    def fechar_comanda(
        self, session: Session, comanda_id: int, estabelecimento_id: int
    ):
        # Lock na comanda para evitar fechamento simultâneo por duas requisições
        comanda = session.exec(
            select(Comanda)
            .where(
                Comanda.id == comanda_id,
                Comanda.estabelecimento_id == estabelecimento_id,
                Comanda.status == "aberta",
            )
            .with_for_update(nowait=False)
        ).first()
        if not comanda:
            raise HTTPException(status_code=404, detail="Comanda não encontrada")

        # Lock nos pedidos para evitar condições de corrida ao verificar status
        pedidos_em_aberto = session.exec(
            select(Pedido)
            .where(
                Pedido.comanda_id == comanda_id,
                Pedido.status.not_in(("CANCELADO", "ENTREGUE")),
            )
            .with_for_update(nowait=False)
        ).all()

        if pedidos_em_aberto:
            raise HTTPException(
                status_code=409,
                detail="Não é possível fechar a comanda. Existem pedidos em aberto.",
            )

        comanda.status = "fechada"
        session.add(comanda)
        session.commit()
        session.refresh(comanda)
        return comanda


comanda_service = ComandaService(Comanda)
