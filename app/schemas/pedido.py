from ..models.pedido import PedidoBase, SQLModel, Optional, Decimal, List, PedidoItem, Field, datetime, timezone

class PedidoCreate(PedidoBase):
    pass

class PedidoRead(PedidoBase):
    id: int
    status: str
    total: Decimal
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    itens: list[PedidoItem] = Field(default_factory=list)

class PedidoUpdate(SQLModel):
    status: Optional[str] = None

class PedidoItemCreate(SQLModel):
    produto_id: int
    quantidade: int
    adicionais: List[int] = Field(default_factory=list)