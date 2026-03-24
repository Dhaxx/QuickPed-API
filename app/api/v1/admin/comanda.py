from fastapi import APIRouter, Depends, status
from app.schemas.comanda import ComandaRead
from app.services.comanda import comanda_service
from app.database.engine import get_session
from app.auth.dependencies import get_current_estabelecimento

router = APIRouter()

@router.get("/", response_model=list[ComandaRead], status_code=status.HTTP_201_CREATED)
def get_comanda( session=Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    return comanda_service.get(session, estabelecimento_id)

@router.put("/", response_model=ComandaRead, status_code=status.HTTP_201_CREATED)
def update_comanda(comanda_id: int, session=Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    return comanda_service.fechar_comanda(session, comanda_id, estabelecimento_id)