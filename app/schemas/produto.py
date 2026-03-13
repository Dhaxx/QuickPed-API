from ..models.produto import ProdutoBase, SQLModel, Optional, Decimal

class ProdutoCreate(ProdutoBase):
    pass

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