from app.models.estabelecimento import Estabelecimento, DiaFuncionamento, dias_default
from app.services.base import BaseService
from sqlmodel import Session, select
from app.models.usuario import Usuario
from ..auth.hash import gerar_hash
import re
import unidecode

class EstabelecimentoService(BaseService[Estabelecimento]):
    def gerar_slug(nome: str) -> str:
        slug = unidecode.unidecode(nome)  # remove acentos
        slug = slug.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)  # substitui espaços e caracteres especiais
        slug = slug.strip('-')
        return slug

    def create(self, session: Session, model_data: dict) -> Estabelecimento:
        if not model_data.get("dias_funcionamento"):
            model_data["dias_funcionamento"] = dias_default()
        
        estabelecimento = Estabelecimento(**model_data)
        estabelecimento.slug = EstabelecimentoService.gerar_slug(estabelecimento.nome)
        session.add(estabelecimento)
        session.flush()

        usuario_admin = Usuario(
            usuario=estabelecimento.cnpj,
            senha_hash=gerar_hash(estabelecimento.cnpj),
            estabelecimento_id=estabelecimento.id
        )
        session.add(usuario_admin)

        session.commit()
        session.refresh(estabelecimento)

        return estabelecimento
    
    def get(self, session: Session, estabelecimento_id: int) -> Estabelecimento:
        stmt = select(self.model).where(self.model.id == estabelecimento_id)
        return session.exec(stmt).one_or_none()
    
    def update(self, session: Session, obj_id: int, model_data: dict) -> Estabelecimento | None:
        obj = session.get(self.model, obj_id)

        if not obj:
            return None
        
        data = model_data

        for column, value in data.items():
            if column == "nome":
                obj.slug = EstabelecimentoService.gerar_slug(value)
            setattr(obj, column, value)

        session.add(obj)
        session.commit()
        session.refresh(obj)

        return obj


# Instância do service
estabelecimento_service = EstabelecimentoService(Estabelecimento)