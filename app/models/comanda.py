from sqlmodel import JSON, Column, Field, SQLModel
from typing import Optional, List, Dict

class Comanda(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id")
    pedidos: List[Dict] = Field(sa_column=Column(JSON))
    em_aberto: bool = True