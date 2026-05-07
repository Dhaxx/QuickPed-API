from app.models.estabelecimento import Estabelecimento, DiaFuncionamento, dias_default
from app.services.base import BaseService
from sqlmodel import Session, select, text
from app.models.usuario import Usuario
from ..auth.admin.hash import gerar_hash
from app.models.parametros import Parametros
import re
import unidecode

class EstabelecimentoService(BaseService[Estabelecimento]):
    query = """select e.*, p.auto_atendimento, p.delivery from estabelecimento e join parametros p on e.id = p.estabelecimento_id where e.id = :estabelecimento_id"""

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
            estabelecimento_id=estabelecimento.id,
            admin=True
        )
        session.add(usuario_admin)
        session.refresh(estabelecimento)

        parametros = Parametros(
            estabelecimento_id=estabelecimento.id, 
            auto_atendimento=model_data.get('auto_atendimento'), 
            delivery=model_data.get('delivery'))
        session.add(parametros)

        session.commit()
        return estabelecimento
    
    def get(self, session: Session, estabelecimento_id: int) -> Estabelecimento:
        response = session.exec(text(self.query), params={"estabelecimento_id": estabelecimento_id}).one_or_none()
        return response
    
    def update(self, session: Session, obj_id: int, model_data: dict) -> Estabelecimento | None:
        obj = session.get(self.model, obj_id)

        if not obj:
            return None
        
        data = model_data

        if "auto_atendimento" in data or "delivery" in data:
            if not obj.parametros:
                obj.parametros = Parametros(estabelecimento_id=obj.id)

            if "auto_atendimento" in data:
                obj.parametros.auto_atendimento = data["auto_atendimento"]

            if "delivery" in data:
                obj.parametros.delivery = data["delivery"]

            data.pop("auto_atendimento", None)
            data.pop("delivery", None)

        for column, value in data.items():
            if column == "nome":
                obj.slug = EstabelecimentoService.gerar_slug(value)
            setattr(obj, column, value)

        session.add(obj)
        session.commit()
        session.refresh(obj)

        return session.exec(text(self.query), params={"estabelecimento_id": obj_id}).one_or_none()  


# Instância do service
estabelecimento_service = EstabelecimentoService(Estabelecimento)