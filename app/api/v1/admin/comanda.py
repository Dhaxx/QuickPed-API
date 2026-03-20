from fastapi import APIRouter, Depends, status
from app.schemas.comanda import ComandaCreate, ComandaRead, ComandaUpdate
from app.services.comanda import comanda_service
from app.database.engine import get_session
from app.auth.dependencies import get_current_estabelecimento

router = APIRouter()

@router.get("/", response_model=list[ComandaRead], status_code=status.HTTP_201_CREATED)
def get_comanda( session=Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    return comanda_service.get(session, estabelecimento_id)

@router.get("/{numero_mesa}", response_model=ComandaRead, status_code=status.HTTP_200_OK)
def get_mesa_comanda(numero_mesa: int, session=Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    return comanda_service.get_by_mesa(session, numero_mesa, estabelecimento_id)