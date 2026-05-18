from sqlmodel import SQLModel


class CardapioPublicResponse(SQLModel):
    estabelecimento: "EstabelecimentoPublic"
    categorias: list["CategoriaPublic"]


class EstabelecimentoPublic(SQLModel):
    nome: str
    aberto: bool  # "aberto" | "fechado"
    slug: str
    logo_url: str | None
    auto_atendimento: bool
    delivery: bool


class CategoriaPublic(SQLModel):
    id: int
    nome: str
    ordem: int
    produtos: list["ProdutoPublic"]


from pydantic import field_serializer
from app.core.config import settings

class ProdutoPublic(SQLModel):
    id: int
    nome: str
    descricao: str | None
    preco: float
    imagem_url: str | None
    disponivel: bool
    adicionais: list["AdicionalPublic"] = []

    @field_serializer("imagem_url")
    def serialize_imagem_url(self, imagem_url: str | None) -> str | None:
        if not imagem_url:
            return None
        if imagem_url.startswith("http://") or imagem_url.startswith("https://"):
            return imagem_url
        
        base_url = settings.CLOUDFLARE_R2_PUBLIC_URL.rstrip("/")
        clean_path = imagem_url.lstrip("/")
        return f"{base_url}/{clean_path}"


class AdicionalPublic(SQLModel):
    id: int
    nome: str
    preco: float
    grupo_id: int | None = None
    grupo_nome: str | None = None
    max_selecoes: int | None = None
    min_selecoes: int | None = None
