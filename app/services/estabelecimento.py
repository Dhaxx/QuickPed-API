from app.models.estabelecimento import Estabelecimento, DiaFuncionamento, dias_default
from app.services.base import BaseService
from sqlmodel import Session
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


# Instância do service
estabelecimento_service = EstabelecimentoService(Estabelecimento)