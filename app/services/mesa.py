from app.models.mesa import Mesa
from app.services.base import BaseService
from sqlmodel import Session, select
from datetime import datetime, timezone

class MesaService(BaseService[Mesa]):
    def get_by_token(self, session: Session, token: str) -> Mesa:
        mesa = session.exec(select(Mesa).where(Mesa.token == token)).first()
        if not mesa:
            raise ValueError("Mesa não encontrada")
        return mesa
    
    def create(self, session, model_data):
        model_data['criado_em'] = datetime.now(timezone.utc)
        return super().create(session, model_data)
    
mesa_service = MesaService(Mesa)