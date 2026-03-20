from fastapi import APIRouter, Depends, status
from app.schemas.produto import GrupoAdicionalCreate, GrupoAdicionalRead, GrupoAdicionalUpdate
from app.services.produto import grupo_adicional_service
from app.auth.dependencies import get_current_estabelecimento
from app.database.engine import get_session

router = APIRouter()

# Rotas dos Grupos de Adicional
@router.post("/", response_model=GrupoAdicionalRead, status_code=status.HTTP_201_CREATED)
def create_grupo_adicional(data: GrupoAdicionalCreate, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    dados = data.model_dump()
    dados["estabelecimento_id"] = estabelecimento_id
    return grupo_adicional_service.create(session, dados)

@router.get("/", response_model=list[GrupoAdicionalRead], status_code=status.HTTP_200_OK)
def get_grupos_adicionais(session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    return grupo_adicional_service.get(session, estabelecimento_id)

@router.put("/", response_model=GrupoAdicionalRead, status_code=status.HTTP_200_OK)
def update_grupo_adicional(grupo_id: int, data: GrupoAdicionalUpdate, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    dados = data.model_dump(exclude_unset=True)
    return grupo_adicional_service.update(session, grupo_id, dados, estabelecimento_id)

@router.delete("/", response_model=GrupoAdicionalRead, status_code=status.HTTP_200_OK)
def delete_grupo_adicional(grupo_id: int, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    return grupo_adicional_service.delete(session, grupo_id, estabelecimento_id)