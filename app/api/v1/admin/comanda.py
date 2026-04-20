from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from app.schemas.comanda import ComandaRead, ComandaUpdate
from app.services.comanda import comanda_service
from app.database.engine import get_session
from app.auth.dependencies import get_current_estabelecimento
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


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
    comanda_id: int = Query(..., description="ID da comanda"),
    body: Optional[ComandaUpdate] = None,
    session=Depends(get_session),
    estabelecimento_id: int = Depends(get_current_estabelecimento),
):
    logger.info(
        f"update_comanda called: comanda_id={comanda_id}, body={body}, forcar={body.forcar if body else None}"
    )
    forcar = body.forcar if body else False
    return comanda_service.fechar_comanda(
        session, comanda_id, estabelecimento_id, forcar
    )
