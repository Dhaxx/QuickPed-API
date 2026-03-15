from app.models.estabelecimento import Estabelecimento, DiaFuncionamento, dias_default
from app.services.base import BaseService
from sqlmodel import Session

class EstabelecimentoService(BaseService[Estabelecimento]):

    def create(self, session: Session, model_data: dict) -> Estabelecimento:
        # Se não vier dias_funcionamento, aplica o padrão
        if not model_data.get("dias_funcionamento"):
            model_data["dias_funcionamento"] = dias_default()
        
        # Cria o objeto
        estabelecimento = Estabelecimento(**model_data)
        session.add(estabelecimento)
        session.commit()
        session.refresh(estabelecimento)

        # Converte cada item do JSON em DiaFuncionamento, garantindo lista de objetos
        estabelecimento.dias_funcionamento = [
            DiaFuncionamento(**d) if isinstance(d, dict) else d
            for d in estabelecimento.dias_funcionamento
        ]

        return estabelecimento


# Instância do service
estabelecimento_service = EstabelecimentoService(Estabelecimento)