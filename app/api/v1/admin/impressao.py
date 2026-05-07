from fastapi import APIRouter, Depends, status
from app.services.impressao import impressao_service
from app.services.pedido import pedido_service
from app.auth.admin.dependencies import get_current_estabelecimento
from app.database.engine import get_session

router = APIRouter()


@router.get("/test")
def test_impressao():
    return {"message": "Rota de impressao funcionando!"}


@router.post("/pedido/{pedido_id}", status_code=status.HTTP_200_OK)
def solicitar_impressao(
    pedido_id: int,
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    session=Depends(get_session),
):
    pedido_service.marcar_impresso(session, pedido_id, estabelecimento_id, False)
    return {"message": "Pedido adicionado na fila de impressão", "pedido_id": pedido_id}


@router.get("/pedido/{pedido_id}", status_code=status.HTTP_200_OK)
def get_texto_impressao(
    pedido_id: int,
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    session=Depends(get_session),
):
    return impressao_service.imprimir_pedido(session, pedido_id, estabelecimento_id)


@router.post("/marcar-impresso/{pedido_id}", status_code=status.HTTP_200_OK)
def marcar_impresso(
    pedido_id: int,
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    session=Depends(get_session),
):
    pedido_service.marcar_impresso(session, pedido_id, estabelecimento_id, True)
    return {"message": "Pedido marcado como impresso"}


@router.get("/comanda/{comanda_id}", status_code=status.HTTP_200_OK)
def get_comanda_impressao(
    comanda_id: int,
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    session=Depends(get_session),
):
    return impressao_service.imprimir_comanda(session, comanda_id, estabelecimento_id)
