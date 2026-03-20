from sqlmodel import Field, SQLModel, Column, Numeric, Relationship, CheckConstraint
from typing import Optional
from enum import Enum
from decimal import Decimal
from .estabelecimento import Estabelecimento

class StatusComanda(str, Enum):
    ABERTA = "aberta"
    FECHADA = "fechada"
    PAGA = "paga"

class ComandaBase(SQLModel):
    numero_mesa: int = Field(index=True)
    status: StatusComanda = Field(default=StatusComanda.ABERTA, index=True)

class Comanda(ComandaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    total: Decimal = Field(default=0.00, sa_column=Column(Numeric(10, 2), CheckConstraint("preco >= 0", name="check_preco_positivo")))
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id")

    estabelecimento: "Estabelecimento" = Relationship(back_populates="comandas")
    pedidos: list["Pedido"] = Relationship(back_populates="comanda")