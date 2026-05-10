from app.models.usuario import Usuario
from app.services.base import BaseService
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from ..auth.admin.hash import gerar_hash, verificar_hash
from fastapi import HTTPException


class UsuarioService(BaseService[Usuario]):
    def autenticar(self, session: Session, usuario: str, senha: str) -> Usuario:
        stmt = (
            select(Usuario)
            .options(selectinload(Usuario.permissoes))
            .where(
                Usuario.admin == True,
                Usuario.usuario == usuario,
            )
        )
        usuario = session.exec(stmt).first()

        if not usuario:
            raise HTTPException(
                status_code=401, detail="Usuário inválido para acesso administrativo"
            )

        if not verificar_hash(senha, usuario.senha_hash):
            raise HTTPException(status_code=401, detail="Senha incorreta")

        if not usuario.ativo:
            raise HTTPException(
                status_code=403, detail="Usuário inativo, contate o administrador"
            )

        return usuario


    def registrar(
        self, session: Session, usuario: str, senha: str, estabelecimento_id: int
    ) -> Usuario:
        senha_hash = gerar_hash(senha)
        novo_usuario = self.create(session, {"usuario": usuario, "senha_hash": senha_hash, "estabelecimento_id": estabelecimento_id})
        self.criar_permissoes_usuario(session, novo_usuario.id)
        return novo_usuario


    def get(self, session: Session, estabelecimento_id: int) -> list[Usuario]:
        stmt = select(Usuario).where(
            Usuario.estabelecimento_id == estabelecimento_id, Usuario.admin == False
        )
        return session.exec(stmt).all()
    

    def criar_permissoes_usuario(self, session: Session, usuario_id: int) -> None:
        """Cria registro padrão de permissões para um novo usuário"""
        from app.models.permissoes import PermissaoUsuario

        # Verifica se já existe
        stmt = select(PermissaoUsuario).where(
            PermissaoUsuario.usuario_id == usuario_id
        )
        if session.exec(stmt).first():
            return
        
        permissao = PermissaoUsuario(usuario_id=usuario_id)
        session.add(permissao)
        session.commit()


autenticacao_service = UsuarioService(Usuario)
