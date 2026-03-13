from sqlmodel import Field, SQLModel
from typing import Optional, List

class CategoriaProduto(SQLModel, table=True):
    __tablename__ = 'categoria_produto' # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    icone: Optional[str] = None
    ordem: int = 0
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id")
    ativo: bool = Field(default=True)