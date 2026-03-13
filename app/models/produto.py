from sqlmodel import SQLModel, Field, Relationship, JSON, Column, Numeric
from typing import Optional, List
from .categoria_produto import CategoriaProduto
from decimal import Decimal

class ProdutoBase(SQLModel):
    nome: str
    descricao: Optional[str] = None
    preco: Decimal = Field(sa_column=Column(Numeric(10,2)))
    imagem_url: Optional[str] = None

class Produto(ProdutoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    categoria_id: int = Field(foreign_key="categoria_produto.id", index=True)
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id", index=True)
    ativo: bool = Field(default=True)

    grupos: List["GrupoAdicional"] = Relationship(back_populates="produto")
    categoria: Optional["CategoriaProduto"] = Relationship(back_populates="produtos")

class GrupoAdicional(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    max_selecoes: int = Field(default=1)
    produto_id: int = Field(foreign_key="produto.id")
    
    produto: "Produto" = Relationship(back_populates="grupos")
    adicionais: List["Adicional"] = Relationship(back_populates="grupo")

class Adicional(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    preco: Decimal = Field(sa_column=Column(Numeric(10,2)))
    grupo_id: int = Field(foreign_key="grupoadicional.id")
    
    grupo: "GrupoAdicional" = Relationship(back_populates="adicionais")