from ..models.usuario import UsuarioBase, SQLModel

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

class UsuarioRead(UsuarioBase):
    id: int
    usuario: str
    estabelecimento_id: int
    ativo: bool
    admin: bool