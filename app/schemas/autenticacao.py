from ..models.usuario import UsuarioBase, SQLModel
from pydantic import field_validator


class LoginRequest(SQLModel):
    usuario: str
    senha: str


class TokenResponse(SQLModel):
    usuario_id: int
    estabelecimento_id: int
    access_token: str
    token_type: str = "bearer"


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
