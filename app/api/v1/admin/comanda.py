from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from app.schemas.comanda import ComandaRead
from app.services.comanda import comanda_service
from app.database.engine import get_session
from app.auth.dependencies import get_current_estabelecimento

router = APIRouter()


@router.get("/", response_model=list[ComandaRead], status_code=status.HTTP_200_OK)
def get_comanda(
    status: Optional[str] = Query(
        None, description="Filtrar por status: 'aberta' ou 'fechada'"
    ),
    session=Depends(get_session),
    estabelecimento_id: int = Depends(get_current_estabelecimento),
):
    return list(comanda_service.get_all(session, estabelecimento_id, status))


@router.put("/", response_model=ComandaRead, status_code=status.HTTP_201_CREATED)
def update_comanda(
    comanda_id: int,
    session=Depends(get_session),
    estabelecimento_id: int = Depends(get_current_estabelecimento),
):
    return comanda_service.fechar_comanda(session, comanda_id, estabelecimento_id)
