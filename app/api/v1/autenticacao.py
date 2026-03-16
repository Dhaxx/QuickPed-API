from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ...database.engine import get_session
from ...schemas.autenticacao import LoginRequest, TokenResponse
from ...services.autenticacao import autenticacao_service
from ...auth.jwt import criar_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, session: Session = Depends(get_session)):
    usuario = autenticacao_service.autenticar(session, data.usuario, data.senha)

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    
    token = criar_token(
        {
            "user_id": usuario.id,
            "estabelecimento_id": usuario.estabelecimento_id
        }
    )

    return {"acess_token": token}