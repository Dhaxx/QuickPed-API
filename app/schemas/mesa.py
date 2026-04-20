from ..models.mesa import MesaBase, Optional, SQLModel, datetime

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