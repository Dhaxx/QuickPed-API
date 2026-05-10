from fastapi import APIRouter, Depends, status
from app.schemas.estabelecimento import (
    EstabelecimentoCreate,
    EstabelecimentoRead,
    EstabelecimentoUpdate,
)
from app.services.estabelecimento import estabelecimento_service
from app.database.engine import get_session
from app.auth.admin.dependencies import get_current_estabelecimento, require_master, require_permission

router = APIRouter()


@router.post(
    "/", response_model=EstabelecimentoRead, status_code=status.HTTP_201_CREATED
)
def create_estabelecimento(
    data: EstabelecimentoCreate,
    session=Depends(get_session),
    current_user=Depends(require_master)
):
    dados = data.model_dump()
    return estabelecimento_service.create(session, dados)


@router.get("/", response_model=EstabelecimentoRead, status_code=status.HTTP_200_OK)
def get_estabelecimento(
    session=Depends(get_session),
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    _=Depends(require_permission("estabelecimentos", "visualizar"))
):
    return estabelecimento_service.get(session, estabelecimento_id)


@router.put("/", response_model=EstabelecimentoRead, status_code=status.HTTP_200_OK)
def update_estabelecimento(
    data: EstabelecimentoUpdate,
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    session=Depends(get_session),
    _=Depends(require_permission("estabelecimentos", "editar"))
):
    dados = data.model_dump(exclude_unset=True)
    return estabelecimento_service.update(session, estabelecimento_id, dados)

