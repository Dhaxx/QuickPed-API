from fastapi import APIRouter, Depends, status
from app.schemas.mesa import MesaCreate, MesaRead, MesaUpdate
from app.services.mesa import mesa_service
from app.auth.dependencies import get_current_estabelecimento
from app.database.engine import get_session

router = APIRouter()

@router.get("/{token}", response_model=MesaRead, status_code=status.HTTP_200_OK)
def get_mesa_by_token(token: str, session=Depends(get_session)):
    return mesa_service.get_by_token(session, token)