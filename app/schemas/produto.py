from ..models.produto import SQLModel, ProdutoBase, GrupoAdicionalBase, AdicionalBase, Optional, Decimal
from pydantic import field_validator

class ProdutoCreate(ProdutoBase):
    @field_validator("preco")
    def preco_nao_negativo(cls, v: Decimal):
        if v < 0:
            raise ValueError("O preço não pode ser negativo")
        return v

class ProdutoRead(ProdutoBase):
    id: int
    ativo: bool

class ProdutoUpdate(SQLModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[Decimal] = None
    imagem_url: Optional[str] = None
    categoria_id: Optional[int] = None
    estabelecimento_id: Optional[int] = None
    ativo: Optional[bool] = None

    @field_validator("preco")
    def preco_nao_negativo(cls, v: Optional[Decimal]):
        if v is None:
            return v
        if v < 0:
            raise ValueError("O preço não pode ser negativo")
        return v


class GrupoAdicionalCreate(GrupoAdicionalBase):
    pass

class GrupoAdicionalRead(GrupoAdicionalBase):
    id: int

class GrupoAdicionalUpdate(SQLModel):
    nome: Optional[str] = None
    max_selecoes: Optional[int] = None

class AdicionalCreate(AdicionalBase):
    grupo_id: int

    @field_validator("preco")
    def preco_nao_negativo(cls, v: Decimal):
        if v < 0:
            raise ValueError("O preço não pode ser negativo")
        return v

class AdicionalRead(AdicionalBase):
    id: int
    grupo_id: int

class AdicionalUpdate(SQLModel):
    nome: Optional[str] = None
    preco: Optional[Decimal] = None
    grupo_id: Optional[int] = None

    @field_validator("preco")
    def preco_nao_negativo(cls, v: Decimal):
        if v < 0:
            raise ValueError("O preço não pode ser negativo")
        return v