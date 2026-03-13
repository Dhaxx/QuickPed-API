from sqlmodel import Column, Field, SQLModel, Numeric, JSON
from typing import Optional, List
from decimal import Decimal
from enum import Enum


class StatusPedido(str, Enum):
    PENDENTE = "Pendente"
    PREPARACAO = "Em Preparação"
    PRONTO = "Pronto"
    ENTREGUE = "Entregue"


class PedidoItemAdicional(SQLModel):
    nome: str
    preco: float


class PedidoItem(SQLModel):
    produto_id: int
    nome_produto: str
    preco_unitario: Decimal
    quantidade: int
    adicionais: List[PedidoItemAdicional] = Field(default_factory=list)


class PedidoBase(SQLModel):
    estabelecimento_id: int
    comanda_id: int = Field(foreign_key="comanda.id", index=True)
    nome_cliente: str
    numero_mesa: int = Field(index=True)

    itens: List[PedidoItem] = Field(
        sa_column=Column(JSON),
        default_factory=list
    )
    total: Decimal = Field(sa_column=Column(Numeric(10, 2)))

    status: StatusPedido = Field(default=StatusPedido.PENDENTE, index=True)


class Pedido(PedidoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)