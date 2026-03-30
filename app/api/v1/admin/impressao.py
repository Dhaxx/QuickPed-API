from fastapi import APIRouter, Depends, status
from app.services.impressao import impressao_service
from app.auth.dependencies import get_current_estabelecimento
from app.database.engine import get_session

router = APIRouter()

@router.post("/Pedido/{pedido_id}", status_code=status.HTTP_200_OK)
def imprimir_pedido(pedido_id: int, estabelecimento_id: int = Depends(get_current_estabelecimento), session=Depends(get_session)) -> None:
    impressao_service.imprimir_pedido(session, pedido_id, estabelecimento_id)
    return None