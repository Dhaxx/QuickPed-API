from sqlmodel import JSON, Column, Field, SQLModel
from typing import Optional, List, Dict

class Pedido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id")
    nome_cliente: str
    numero_mesa: int
    itens: List[Dict] = Field(sa_column=Column(JSON), default=[])
    total: float
    status: str = Field(default="Pendente")  # Pendente, Em Preparação, Pronto, Entregue