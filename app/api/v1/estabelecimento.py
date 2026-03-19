from fastapi import APIRouter, Depends, status
from ...schemas.estabelecimento import EstabelecimentoCreate, EstabelecimentoRead, EstabelecimentoUpdate
from ...services.estabelecimento import estabelecimento_service
from ...database.engine import get_session
from ...auth.dependencies import get_current_estabelecimento

router = APIRouter()

# @router.post("/", response_model=EstabelecimentoRead, status_code=status.HTTP_201_CREATED)
# def create_estabelecimento(
#     data: EstabelecimentoCreate,
#     session = Depends(get_session)
# ):
#     dados = data.model_dump()
#     return estabelecimento_service.create(session, dados)

# @router.get("/", response_model=list[EstabelecimentoRead], status_code=status.HTTP_200_OK)
# def get_estabelecimentos(
#     session = Depends(get_session)
# ):
#     return estabelecimento_service.get(session)

# @router.get("/{estabelecimento_id}", response_model=EstabelecimentoRead, status_code=status.HTTP_200_OK)
# def get_estabelecimento(
#     estabelecimento_id: int,
#     session = Depends(get_session)
# ):
#     return estabelecimento_service.get(session, estabelecimento_id)

@router.put("/", response_model=EstabelecimentoRead, status_code=status.HTTP_200_OK)
def update_estabelecimento(
    data: EstabelecimentoUpdate,
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    session = Depends(get_session)
):
    dados = data.model_dump(exclude_unset=True)
    return estabelecimento_service.update(session, dados, estabelecimento_id)

# @router.delete("/{estabelecimento_id}", response_model=EstabelecimentoRead, status_code=status.HTTP_200_OK)
# def delete_estabelecimento(
#     estabelecimento_id: int,
#     session = Depends(get_session)
# ):
#     return estabelecimento_service.delete(session, estabelecimento_id)