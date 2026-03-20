from fastapi import APIRouter, Depends, status
from app.schemas.produto import AdicionalCreate, AdicionalRead, AdicionalUpdate
from app.services.produto import adicional_service
from app.auth.dependencies import get_current_estabelecimento
from app.database.engine import get_session

router = APIRouter()

# Rotas dos Adicionais
@router.post("/", response_model=AdicionalRead, status_code=status.HTTP_201_CREATED)
def create_adicional(data: AdicionalCreate, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    dados = data.model_dump()
    dados["estabelecimento_id"] = estabelecimento_id
    return adicional_service.create(session, dados)

@router.get("/", response_model=list[AdicionalRead], status_code=status.HTTP_200_OK)
def get_adicionais(session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    return adicional_service.get(session, estabelecimento_id)

@router.put("/", response_model=AdicionalRead, status_code=status.HTTP_200_OK)
def update_adicional(adicional_id: int, data: AdicionalUpdate, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    dados = data.model_dump(exclude_unset=True)
    return adicional_service.update(session, adicional_id, dados, estabelecimento_id)

@router.delete("/", response_model=AdicionalRead, status_code=status.HTTP_200_OK)
def delete_adicional(adicional_id: int, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    return adicional_service.delete(session, adicional_id, estabelecimento_id)