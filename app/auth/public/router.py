from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlmodel import Session
from ...database.engine import get_session
from ...schemas.cliente import (
    ClienteTokenResponse,
    ClienteCreate,
    ClienteRead,
)
from ...services.cliente import cliente_service
from ...auth.jwt import criar_token

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)

@router.post("/login", response_model=ClienteTokenResponse)
@limiter.limit("5/15minutes")
def login(
    request: Request,
    telefone: str,
    session: Session = Depends(get_session),
):
    cliente = cliente_service.autenticar(
        session, telefone
    )

    if not cliente:
        raise HTTPException(status_code=401, detail="Telefone ou senha inválidos")

    token = criar_token({"cliente_id": cliente.id})

    return {
        "access_token": token,
        "cliente_id": cliente.id,
        "token_type": "bearer",
        "nome": cliente.nome
    }

@router.post("/registrar", response_model=ClienteRead)
def registrar(
    data: ClienteCreate,
    session: Session = Depends(get_session),
):
    dados = data.model_dump()
    return cliente_service.create(session, dados)