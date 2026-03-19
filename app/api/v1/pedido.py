from fastapi import APIRouter, Depends, status
from ...schemas.pedido import PedidoCreate, PedidoRead, PedidoUpdate
from ...services.pedido import pedido_service
from ...auth.dependencies import get_current_estabelecimento
from ...database.engine import get_session

router = APIRouter()

# Rotas dos Pedidos
@router.get("/", response_model=list[PedidoRead], status_code=status.HTTP_200_OK)
def get_Pedidos( session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento) ):
    return pedido_service.get(session, estabelecimento_id)

@router.put("/", response_model=PedidoRead, status_code=status.HTTP_200_OK)
def update_Pedido( Pedido_id: int, data: PedidoUpdate, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    dados = data.model_dump(exclude_unset=True)
    return pedido_service.update(session, Pedido_id, dados, estabelecimento_id)

@router.delete("/", response_model=PedidoRead, status_code=status.HTTP_200_OK)
def update_Pedido( Pedido_id: int, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    return pedido_service.delete(session, Pedido_id, estabelecimento_id)