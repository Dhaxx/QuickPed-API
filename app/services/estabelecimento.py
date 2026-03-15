from app.models.estabelecimento import Estabelecimento
from app.schemas.estabelecimento import EstabelecimentoCreate, EstabelecimentoUpdate
from app.services.base import BaseService

estabelecimento_service = BaseService(
    Estabelecimento,
    EstabelecimentoCreate, 
    EstabelecimentoUpdate
)