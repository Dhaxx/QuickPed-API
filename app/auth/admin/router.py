from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlmodel import Session
from ...database.engine import get_session
from ...schemas.autenticacao import (
    UsuarioLoginRead,
    UsuarioCreate,
    UsuarioRead,
)
from ...services.autenticacao import autenticacao_service
from ..jwt import criar_token
from .dependencies import get_current_estabelecimento, require_permission

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)


@router.post("/login", response_model=UsuarioLoginRead)
@limiter.limit("5/15minutes")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    usuario = autenticacao_service.autenticar(
        session, form_data.username, form_data.password
    )

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    token = criar_token(
        {"user_id": usuario.id, "estabelecimento_id": usuario.estabelecimento_id}
    )

    return UsuarioLoginRead(
        access_token=token,
        usuario_id=usuario.id,
        estabelecimento_id=usuario.estabelecimento_id,
        permissoes=usuario.permissoes,
    )


@router.post("/registrar", response_model=UsuarioRead)
def registrar(
    data: UsuarioCreate,
    session: Session = Depends(get_session),
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    _=Depends(require_permission("usuarios", "editar"))
):
    usuario = autenticacao_service.registrar(
        session, data.usuario, data.senha, estabelecimento_id
    )

    if not usuario:
        raise HTTPException(status_code=400, detail="Erro ao registrar usuário")

    return usuario


@router.get("/usuarios", response_model=list[UsuarioRead])
def listar_usuarios(
    session: Session = Depends(get_session),
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    _=Depends(require_permission("usuarios", "visualizar"))
):
    return autenticacao_service.get(session, estabelecimento_id)
