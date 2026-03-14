from ..models.comanda import ComandaBase, SQLModel, Optional, StatusComanda

class ComandaCreate(ComandaBase):
    estabelecimento_id: int
    numero_mesa: int

class ComandaRead(ComandaBase):
    id: int

class ComandaUpdate(SQLModel):
    estabelecimento_id: Optional[int] = None
    numero_mesa: Optional[int] = None
    status: Optional[StatusComanda] = None