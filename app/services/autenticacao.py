from app.models.usuario import Usuario
from app.services.base import BaseService
from sqlmodel import Session
from ..auth.hash import verificar_hash

class UsuarioService(BaseService[Usuario]):
    def autenticar(self, session: Session, usuario: str, senha: str) -> Usuario:
        usuario = session.get(Usuario, usuario)

        if not usuario:
            return None
        
        if not verificar_hash(senha, usuario.senha):
            return None

        return usuario
    
autenticacao_service = UsuarioService(Usuario)