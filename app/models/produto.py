from sqlmodel import SQLModel, Field, Relationship, JSON, Column, Numeric, CheckConstraint
from typing import Optional, List
from .categoria_produto import CategoriaProduto
from decimal import Decimal
from .estabelecimento import Estabelecimento

class ProdutoBase(SQLModel):
    nome: str
    descricao: Optional[str] = None
    preco: Decimal = Field(sa_column=Column(Numeric(10,2), CheckConstraint("preco >= 0", name="check_preco_positivo")))
    imagem_url: Optional[str] = None
    categoria_id: int = Field(foreign_key="categoria_produto.id", index=True)

class Produto(ProdutoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    estabelecimento_id: int = Field(foreign_key="estabelecimento.id", index=True)
    ativo: bool = Field(default=True)

    grupos: List["GrupoAdicional"] = Relationship(back_populates="produto")
    categoria: Optional["CategoriaProduto"] = Relationship(back_populates="produtos")

class GrupoAdicionalBase(SQLModel):
    nome: str
    max_selecoes: int = Field(default=1)
    produto_id: int = Field(foreign_key="produto.id")

class GrupoAdicional(GrupoAdicionalBase, table=True):
    __tablename__ = "grupo_adicional"
    id: Optional[int] = Field(default=None, primary_key=True)
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id", index=True)
    
    produto: "Produto" = Relationship(back_populates="grupos")
    adicionais: List["Adicional"] = Relationship(back_populates="grupo")
    estabelecimento: "Estabelecimento" = Relationship( back_populates="grupos_adicionais" )

class AdicionalBase(SQLModel):
    nome: str
    preco: Decimal = Field(sa_column=Column(Numeric(10,2), CheckConstraint("preco >= 0", name="check_preco_positivo")))

class Adicional(AdicionalBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    grupo_id: int = Field(foreign_key="grupo_adicional.id")
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id", index=True)

    estabelecimento: "Estabelecimento" = Relationship( back_populates="adicionais" )
    grupo: "GrupoAdicional" = Relationship(back_populates="adicionais")