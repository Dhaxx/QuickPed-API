from sqlmodel import JSON, Column, Field, SQLModel
from typing import Optional, List, Dict
from enum import Enum

class StatusComanda(str, Enum):
    ABERTA = "aberta"
    FECHADA = "fechada"
    PAGA = "paga"

class ComandaBase(SQLModel):
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id")
    numero_mesa: int = Field(index=True)
    status: StatusComanda = Field(default=StatusComanda.ABERTA, index=True)

class Comanda(ComandaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)