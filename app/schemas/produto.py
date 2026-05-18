from ..models.produto import (
    SQLModel,
    ProdutoBase,
    GrupoAdicionalBase,
    AdicionalBase,
    Optional,
    Decimal,
)
from pydantic import field_validator
from fastapi import UploadFile


class ProdutoCreate(ProdutoBase):
    imagem_file: Optional[UploadFile] = None

    @field_validator("preco")
    def preco_nao_negativo(cls, v: Decimal):
        if v < 0:
            raise ValueError("O preço não pode ser negativo")
        return v


from pydantic import field_serializer
from app.core.config import settings

class ProdutoRead(ProdutoBase):
    id: int
    ativo: bool

    @field_serializer("imagem_url")
    def serialize_imagem_url(self, imagem_url: Optional[str]) -> Optional[str]:
        if not imagem_url:
            return None
        if imagem_url.startswith("http://") or imagem_url.startswith("https://"):
            return imagem_url
        
        base_url = settings.CLOUDFLARE_R2_PUBLIC_URL.rstrip("/")
        clean_path = imagem_url.lstrip("/")
        return f"{base_url}/{clean_path}"


class ProdutoUpdate(SQLModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[Decimal] = None
    imagem_url: Optional[str] = None
    categoria_id: Optional[int] = None
    estabelecimento_id: Optional[int] = None
    ativo: Optional[bool] = None
    imprime: Optional[bool] = None
    produzido_por: Optional[int] = None
    imagem_file: Optional[UploadFile] = None

    @field_validator("preco")
    def preco_nao_negativo(cls, v: Optional[Decimal]):
        if v is None:
            return v
        if v < 0:
            raise ValueError("O preço não pode ser negativo")
        return v


class GrupoAdicionalCreate(GrupoAdicionalBase):
    adicionais: Optional[list["AdicionalBase"]] = None


class GrupoAdicionalRead(GrupoAdicionalBase):
    id: int
    adicionais: list["AdicionalRead"] = []


class GrupoAdicionalUpdate(SQLModel):
    nome: Optional[str] = None
    max_selecoes: Optional[int] = None
    min_selecoes: Optional[int] = None


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

    @field_validator("preco")
    def preco_nao_negativo(cls, v: Decimal):
        if v < 0:
            raise ValueError("O preço não pode ser negativo")
        return v
