from ..models.comanda import ComandaBase, SQLModel, Optional, StatusComanda, Decimal

class ComandaCreate(ComandaBase):
    estabelecimento_id: int
    numero_mesa: int

class ComandaRead(ComandaBase):
    id: int
    total: Decimal

class ComandaUpdate(SQLModel):
    status: Optional[StatusComanda] = None