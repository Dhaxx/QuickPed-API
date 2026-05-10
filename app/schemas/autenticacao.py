from ..models.usuario import UsuarioBase, SQLModel
from pydantic import field_validator
from ..models.permissoes import PermissoesEnum


class LoginRequest(SQLModel):
    usuario: str
    senha: str


class UsuarioCreate(UsuarioBase):
    usuario: str
    senha: str

    @field_validator("senha")
    def senha_minima(cls, v: str):
        if len(v) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres")
        return v


class UsuarioRead(UsuarioBase):
    id: int
    usuario: str
    estabelecimento_id: int
    ativo: bool
    admin: bool


class PermissoesRead(SQLModel):
    dashboard: PermissoesEnum
    pedidos: PermissoesEnum
    comandas: PermissoesEnum
    produtos: PermissoesEnum
    mesas: PermissoesEnum
    estabelecimento: PermissoesEnum
    usuarios: PermissoesEnum


class UsuarioLoginRead(SQLModel):
    access_token: str
    token_type: str = "bearer"
    usuario_id: int
    estabelecimento_id: int
    permissoes: PermissoesRead