from ..models.pedido import PedidoBase, SQLModel, Optional, Decimal, List, PedidoItem, Field, JSON, Column, PedidoItemAdicional

class PedidoCreate(PedidoBase):
    pass

class PedidoRead(PedidoBase):
    id: int
    status: str
    total: Decimal
    criado_em: str
    itens: list[PedidoItem] = Field(default_factory=list)

class PedidoUpdate(SQLModel):
    status: Optional[str] = None

class PedidoItemCreate(SQLModel):
    produto_id: int
    quantidade: int
    adicionais: List[PedidoItemAdicional] = Field(default_factory=list)