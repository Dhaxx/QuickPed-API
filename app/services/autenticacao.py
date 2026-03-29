from app.models.usuario import Usuario
from app.services.base import BaseService
from sqlmodel import Session, select
from ..auth.hash import gerar_hash, verificar_hash
from fastapi import HTTPException

class UsuarioService(BaseService[Usuario]):
    def autenticar(self, session: Session, usuario: str, senha: str) -> Usuario:
        stmt = select(Usuario).where(Usuario.usuario == usuario and Usuario.admin == True)
        usuario = session.exec(stmt).first()

        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário inválido para acesso administrativo")
        
        if not verificar_hash(senha, usuario.senha_hash):
            raise HTTPException(status_code=401, detail="Senha incorreta")
        
        if not usuario.ativo:
            raise HTTPException(status_code=403, detail="Usuário inativo, contate o administrador")

        return usuario
    
    def registrar(self, session: Session, usuario: str, senha: str, estabelecimento_id: int) -> Usuario:
        senha_hash = gerar_hash(senha)
        return self.create(session, {"usuario": usuario, "senha_hash": senha_hash, "estabelecimento_id": estabelecimento_id})
    
    def get(self, session: Session, estabelecimento_id: int) -> list[Usuario]:
        stmt = select(Usuario).where(Usuario.estabelecimento_id == estabelecimento_id, Usuario.admin == False)
        return session.exec(stmt).all()

autenticacao_service = UsuarioService(Usuario)