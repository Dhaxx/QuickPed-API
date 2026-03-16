from ..models.usuario import UsuarioBase

class LoginRequest(UsuarioBase):
    usuario: str
    senha: str

class TokenResponse(UsuarioBase):
    access_token: str
    token_type: str = "bearer"