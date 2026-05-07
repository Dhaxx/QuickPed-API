from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import Session
from ...database.engine import get_session
from app.auth.jwt import SECRET_KEY, ALGORITHM
from app.models.cliente import Cliente

bearer_scheme = HTTPBearer()

def get_current_cliente(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(get_session),
) -> Cliente:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cliente_id = payload.get("cliente_id")
        if not cliente_id:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    cliente = session.get(Cliente, int(cliente_id))
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return cliente