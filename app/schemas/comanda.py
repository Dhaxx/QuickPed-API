from ..models.comanda import ComandaBase, SQLModel, Optional, StatusComanda, Decimal
from ..schemas.pedido import PedidoRead

class ComandaCreate(ComandaBase):
    estabelecimento_id: int
    numero_mesa: int

class ComandaRead(ComandaBase):
    id: int
    total: Decimal
    pedidos: list["PedidoRead"] = []

class ComandaUpdate(SQLModel):
    status: StatusComanda