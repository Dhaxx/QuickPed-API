from app.models.usuario import Usuario
from app.services.base import BaseService
from sqlmodel import Session, select
from ..auth.hash import gerar_hash, verificar_hash

class UsuarioService(BaseService[Usuario]):
    def autenticar(self, session: Session, usuario: str, senha: str) -> Usuario:
        stmt = select(Usuario).where(Usuario.usuario == usuario)
        usuario = session.exec(stmt).first()

        if not usuario:
            return None
        
        if not verificar_hash(senha, usuario.senha_hash):
            return None

        return usuario
    
    def registrar(self, session: Session, usuario: str, senha: str, estabelecimento_id: int) -> Usuario:
        senha_hash = gerar_hash(senha)
        return self.create(session, {"usuario": usuario, "senha_hash": senha_hash, "estabelecimento_id": estabelecimento_id})

autenticacao_service = UsuarioService(Usuario)