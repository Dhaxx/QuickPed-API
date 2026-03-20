from fastapi import APIRouter, Depends, status
from app.schemas.mesa import MesaCreate, MesaRead, MesaUpdate
from app.services.mesa import mesa_service
from app.auth.dependencies import get_current_estabelecimento
from app.database.engine import get_session

router = APIRouter()

@router.post("/", response_model=MesaCreate, status_code=status.HTTP_201_CREATED)
def create_mesa(data: MesaCreate, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    dados = data.model_dump()
    dados["estabelecimento_id"] = estabelecimento_id
    return mesa_service.create(session, dados)

@router.get("/", response_model=list[MesaRead], status_code=status.HTTP_200_OK)
def get_mesas( session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento) ):
    return mesa_service.get(session, estabelecimento_id)

@router.put("/", response_model=MesaRead, status_code=status.HTTP_200_OK)
def update_mesa( mesa_id: int, data: MesaUpdate, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    dados = data.model_dump(exclude_unset=True)
    return mesa_service.update(session, mesa_id, dados, estabelecimento_id)

@router.delete("/", response_model=MesaRead, status_code=status.HTTP_200_OK)
def delete_mesa( mesa_id: int, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    return mesa_service.delete(session, mesa_id, estabelecimento_id)