from fastapi import APIRouter, Depends, status
from app.schemas.comanda import ComandaRead
from app.services.comanda import comanda_service
from app.database.engine import get_session

router = APIRouter()

@router.get("/", response_model=ComandaRead, status_code=status.HTTP_200_OK)
def get_mesa_comanda(token: str, session=Depends(get_session)):
    return comanda_service.get_by_mesa(session, token)