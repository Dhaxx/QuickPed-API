from fastapi import APIRouter, Depends, status
from ...schemas.estabelecimento import EstabelecimentoCreate, EstabelecimentoRead
from ...services.estabelecimento import estabelecimento_service
from ...database.engine import get_session

router = APIRouter()

@router.post("/", response_model=EstabelecimentoRead, status_code=status.HTTP_201_CREATED)
def create_estabelecimento(
    data: EstabelecimentoCreate,
    session = Depends(get_session)
):
    dados = data.model_dump()
    return estabelecimento_service.create(session, dados)

@router.get("/all", response_model=list[EstabelecimentoRead], status_code=status.HTTP_200_OK)
def get_estabelecimentos(
    session = Depends(get_session)
):
    return estabelecimento_service.get_all(session)

@router.get("/{estabelecimento_id}", response_model=EstabelecimentoRead, status_code=status.HTTP_200_OK)
def get_estabelecimento(
    estabelecimento_id: int,
    session = Depends(get_session)
):
    return estabelecimento_service.get(session, estabelecimento_id)

@router.put("/{estabelecimento_id}", response_model=EstabelecimentoRead, status_code=status.HTTP_200_OK)
def update_estabelecimento(
    estabelecimento_id: int,
    data: EstabelecimentoCreate,
    session = Depends(get_session)
):
    dados = data.model_dump()
    return estabelecimento_service.update(session, estabelecimento_id, dados)

@router.delete("/{estabelecimento_id}", response_model=EstabelecimentoRead, status_code=status.HTTP_200_OK)
def delete_estabelecimento(
    estabelecimento_id: int,
    session = Depends(get_session)
):
    return estabelecimento_service.delete(session, estabelecimento_id)