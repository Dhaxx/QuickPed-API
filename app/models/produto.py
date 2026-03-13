from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from typing import Optional, List, Dict
from .categoria_produto import CategoriaProduto

class Produto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: Optional[str] = None
    preco: float
    imagem_url: Optional[str] = None
    adicionais: List[Dict] = Field(sa_column=Column(JSON), default=[])
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria_produto.id")
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id")
    ativo: bool = Field(default=True)

    categoria: Optional["CategoriaProduto"] = Relationship(back_populates="produtos")