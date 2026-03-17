from app.models.estabelecimento import Estabelecimento, DiaFuncionamento, dias_default
from app.services.base import BaseService
from sqlmodel import Session
from app.models.usuario import Usuario
from ..auth.hash import gerar_hash

class EstabelecimentoService(BaseService[Estabelecimento]):

    def create(self, session: Session, model_data: dict) -> Estabelecimento:
        # Se não vier dias_funcionamento, aplica o padrão
        if not model_data.get("dias_funcionamento"):
            model_data["dias_funcionamento"] = dias_default()
        
        # Cria o objeto
        estabelecimento = Estabelecimento(**model_data)
        session.add(estabelecimento)
        session.flush()

        # estabelecimento.dias_funcionamento = [
        #     DiaFuncionamento(**d) if isinstance(d, dict) else d
        #     for d in estabelecimento.dias_funcionamento
        # ]

        usuario_admin = Usuario(
            usuario=estabelecimento.cnpj,  # Usando o CNPJ como nome de usuário
            senha_hash=gerar_hash(estabelecimento.cnpj),  # Senha padrão, deve ser alterada depois
            estabelecimento_id=estabelecimento.id
        )
        session.add(usuario_admin)

        session.commit()
        session.refresh(estabelecimento)

        return estabelecimento


# Instância do service
estabelecimento_service = EstabelecimentoService(Estabelecimento)