from ..models.pedido import PedidoBase, SQLModel, Optional, Decimal, List, PedidoItem, Field, JSON, Column, PedidoItemAdicional

class PedidoCreate(PedidoBase):
    pass

class PedidoRead(PedidoBase):
    id: int
    numero_mesa: int
    nome_cliente: str
    itens: List[PedidoItem] = Field(
        sa_column=Column(JSON),
        default_factory=list
    )

class PedidoUpdate(SQLModel):
    nome_cliente: Optional[str] = None
    numero_mesa: Optional[int] = None
    itens: Optional[List[PedidoItemAdicional]] = None
    total: Optional[Decimal] = None
    status: Optional[str] = None