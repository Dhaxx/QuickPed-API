from sqlmodel import SQLModel

class CardapioPublicResponse(SQLModel):
    estabelecimento: "EstabelecimentoPublic"
    categorias: list["CategoriaPublic"]

class EstabelecimentoPublic(SQLModel):
    id: int
    nome: str
    status: str  # "aberto" | "fechado"

class CategoriaPublic(SQLModel):
    id: int
    nome: str
    ordem: int
    produtos: list["ProdutoPublic"]

class ProdutoPublic(SQLModel):
    id: int
    nome: str
    descricao: str | None
    preco: float
    imagem_url: str | None
    disponivel: bool
    adicionais: list["AdicionalPublic"] = []

class AdicionalPublic(SQLModel):
    id: int
    nome: str
    preco: float