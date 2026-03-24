from ..models.estabelecimento import EstabelecimentoBase, DiaFuncionamento, Optional, List, EmailStr, SQLModel

class EstabelecimentoCreate(EstabelecimentoBase):
    dias_funcionamento: Optional[List[DiaFuncionamento]] = None
    
class EstabelecimentoRead(EstabelecimentoBase):
    id: int
    nome: str
    telefone: str
    dias_funcionamento: List[DiaFuncionamento]
    esta_aberto: bool
    slug: str
    logo_url: Optional[str] = None

class EstabelecimentoUpdate(SQLModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    logo_url: Optional[str] = None
    esta_aberto: Optional[bool] = None