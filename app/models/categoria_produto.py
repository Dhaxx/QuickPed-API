from sqlmodel import Field, SQLModel
from typing import Optional, List

class CategoriaProduto(SQLModel, table=True):
    __tablename__ = 'categoria_produto'
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    icone: Optional[str] = None
    ordem: int = 0
    ativo: bool = Field(default=True)