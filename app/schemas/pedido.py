from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime
from app.core.config import settings


class PedidoCreate(SQLModel):
    nome_cliente: str
    numero_mesa: int
    obs: Optional[str] = None
    mesa_token: Optional[str] = None
    itens: list = Field(default_factory=list)


class PedidoRead(SQLModel):
    id: int
    nome_cliente: str
    numero_mesa: int
    obs: Optional[str] = None
    status: str
    total: Decimal
    criado_em: datetime = Field(default_factory=settings.time_now)
    itens: list = Field(default_factory=list)


class PedidoUpdate(SQLModel):
    status: Optional[str] = None
    oculto: Optional[bool] = None