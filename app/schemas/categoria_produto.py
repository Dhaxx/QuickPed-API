from ..models.categoria_produto import CategoriaProdutoBase, Optional, SQLModel

class CategoriaProdutoCreate(CategoriaProdutoBase):
    pass

class CategoriaProdutoRead(CategoriaProdutoBase):
    id: int
    nome: str
    icone: Optional[str] = None

class CategoriaProdutoUpdate(SQLModel):
    nome: Optional[str] = None
    icone: Optional[str] = None
    ordem: Optional[int] = None
    ativo: Optional[bool] = None