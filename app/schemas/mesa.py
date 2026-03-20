from ..models.mesa import MesaBase, Optional, SQLModel, Field, datetime, uuid

class MesaCreate(MesaBase):
    pass

class MesaRead(MesaBase):
    id: int
    token: str
    ativa: bool
    criado_em: Optional[datetime] = None

class MesaUpdate(SQLModel):
    numero: Optional[int] = None
    ativa: Optional[bool] = None