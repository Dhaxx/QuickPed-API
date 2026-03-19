from ..models.produto import SQLModel, ProdutoBase, GrupoAdicionalBase, AdicionalBase, Optional, Decimal

class ProdutoCreate(ProdutoBase):
    caregoria_id: int

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

class GrupoAdicionalCreate(GrupoAdicionalBase):
    pass

class GrupoAdicionalRead(GrupoAdicionalBase):
    id: int

class GrupoAdicionalUpdate(SQLModel):
    nome: Optional[str] = None
    max_selecoes: Optional[int] = None

class AdicionalCreate(AdicionalBase):
    grupo_id: int

class AdicionalRead(AdicionalBase):
    id: int
    grupo_id: int

class AdicionalUpdate(SQLModel):
    nome: Optional[str] = None
    preco: Optional[Decimal] = None
    grupo_id: Optional[int] = None