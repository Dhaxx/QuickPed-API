from sqlmodel import Column, Field, SQLModel, Numeric, JSON, Relationship
from typing import Optional, List
from decimal import Decimal
from enum import Enum
from datetime import datetime
from .estabelecimento import Estabelecimento
from .comanda import Comanda

class StatusPedido(str, Enum):
    PENDENTE = "Pendente"
    PREPARACAO = "Em Preparação"
    PRONTO = "Pronto"
    ENTREGUE = "Entregue"
    CANCELADO = "Cancelado"


class PedidoItemAdicional(SQLModel):
    nome: str
    preco: Decimal = Field(sa_column=Column(Numeric(10,2)))


class PedidoItem(SQLModel):
    produto_id: int
    nome_produto: str
    preco_unitario: Decimal = Field(sa_column=Column(Numeric(10,2)))
    quantidade: int
    adicionais: List[PedidoItemAdicional] = Field(default_factory=list)


class PedidoBase(SQLModel):
    nome_cliente: str
    numero_mesa: int = Field(index=True)
    obs: Optional[str] = None

    itens: List[PedidoItem] = Field(
        sa_column=Column(JSON),
        default_factory=list
    )

class Pedido(PedidoBase, table=True):
    id: int = Field(primary_key=True)
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id", index=True)
    comanda_id: int = Field(foreign_key="comanda.id", index=True)
    status: StatusPedido = Field(default=StatusPedido.PENDENTE, index=True)
    criado_em: datetime = Field(default_factory=datetime.now())
    total: Decimal = Field(sa_column=Column(Numeric(10, 2)))

    estabelecimento: "Estabelecimento" = Relationship(back_populates="pedidos")
    comanda: "Comanda" = Relationship(back_populates="pedidos")