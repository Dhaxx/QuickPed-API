from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from app.schemas.comanda import ComandaRead, ComandaUpdate
from app.services.comanda import comanda_service
from app.database.engine import get_session
from app.auth.admin.dependencies import get_current_estabelecimento, require_permission
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
    _=Depends(require_permission("comandas", "visualizar"))
):
    return list(comanda_service.get_all(session, estabelecimento_id, status))


@router.get(
    "/para-imprimir", response_model=list[ComandaRead], status_code=status.HTTP_200_OK
)
def get_comandas_para_imprimir(
    session=Depends(get_session),
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    _=Depends(require_permission("comandas", "visualizar"))
):
    return list(comanda_service.get_para_imprimir(session, estabelecimento_id))


@router.post("/imprimir/{comanda_id}", status_code=status.HTTP_200_OK)
def solicitar_impressao_comanda(
    comanda_id: int,
    session=Depends(get_session),
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    _=Depends(require_permission("comandas", "editar"))
):
    comanda_service.marcar_impresso(session, comanda_id, estabelecimento_id, True)
    return {
        "message": "Comanda adicionada na fila de impressão",
        "comanda_id": comanda_id,
    }


@router.post("/impresso/{comanda_id}", status_code=status.HTTP_200_OK)
def marcar_comanda_impressa(
    comanda_id: int,
    session=Depends(get_session),
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    _=Depends(require_permission("comandas", "editar"))
):
    comanda_service.marcar_impresso(session, comanda_id, estabelecimento_id, False)
    return {"message": "Comanda marcada como impressa"}


@router.put("/", response_model=ComandaRead, status_code=status.HTTP_201_CREATED)
def update_comanda(
    comanda_id: int = Query(..., description="ID da comanda"),
    body: Optional[ComandaUpdate] = None,
    session=Depends(get_session),
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    _=Depends(require_permission("comandas", "editar"))
):
    logger.info(
        f"update_comanda called: comanda_id={comanda_id}, body={body}, forcar={body.forcar if body else None}"
    )
    forcar = body.forcar if body else False
    return comanda_service.fechar_comanda(
        session, comanda_id, estabelecimento_id, forcar
    )
