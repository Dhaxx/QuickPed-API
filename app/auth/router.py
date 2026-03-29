from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database.engine import get_session
from ..schemas.autenticacao import LoginRequest, TokenResponse, UsuarioCreate, UsuarioRead
from ..services.autenticacao import autenticacao_service
from ..auth.jwt import criar_token
from ..auth.dependencies import get_current_estabelecimento

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    usuario = autenticacao_service.autenticar(session, form_data.username, form_data.password)

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    
    token = criar_token(
        {
            "user_id": usuario.id,
            "estabelecimento_id": usuario.estabelecimento_id
        }
    )

    return {"access_token": token, "usuario_id": usuario.id, "estabelecimento_id": usuario.estabelecimento_id}

@router.post("/registrar", response_model=UsuarioRead)
def registrar(data: UsuarioCreate, session: Session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    usuario = autenticacao_service.registrar(session, data.usuario, data.senha, estabelecimento_id)

    if not usuario:
        raise HTTPException(status_code=400, detail="Erro ao registrar usuário")

    return usuario

@router.get("/usuarios", response_model=list[UsuarioRead])
def listar_usuarios(session: Session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    return autenticacao_service.get(session, estabelecimento_id)