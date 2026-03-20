from fastapi import APIRouter, Depends, status
from sqlmodel import select
from app.schemas.pedido import PedidoCreate, PedidoRead
from app.services.pedido import pedido_service
from app.models.estabelecimento import Estabelecimento
from app.database.engine import get_session

router = APIRouter()

# Rotas dos Pedidos
@router.post("/", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def create_Pedido( data: PedidoCreate, session = Depends(get_session), slug: str = None):
    stmt = select(Estabelecimento.id).where(Estabelecimento.slug == slug)
    estabelecimento_id = session.exec(stmt).first()

    return pedido_service.create(session, estabelecimento_id, data)

@router.get("/{mesa_token}", response_model=list[PedidoRead], status_code=status.HTTP_200_OK)
def get_Pedidos(session = Depends(get_session), slug: str = None, mesa_token: str = None):
    stmt = select(Estabelecimento.id).where(Estabelecimento.slug == slug)
    estabelecimento_id = session.exec(stmt).first()
    return pedido_service.get_by_comanda(session, mesa_token, estabelecimento_id)