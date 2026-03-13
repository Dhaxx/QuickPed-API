from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from .estabelecimento import Estabelecimento

class CategoriaProdutoBase(SQLModel):
    nome: str
    icone: Optional[str] = None
    ordem: int = Field(default=0)
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id", index=True)

class CategoriaProduto(CategoriaProdutoBase, table=True):
    __tablename__ = 'categoria_produto'
    id: Optional[int] = Field(default=None, primary_key=True)

    ativo: bool = Field(default=True)

    estabelecimento: "Estabelecimento" = Relationship(back_populates="categorias")
    produtos: list["Produto"] = Relationship(back_populates="categoria")