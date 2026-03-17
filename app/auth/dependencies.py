from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlmodel import Session

from ..database.engine import get_session
from app.models.usuario import Usuario
from app.auth.jwt import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/autenticacao/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> Usuario:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = db.get(Usuario, int(user_id))
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return user

def get_current_estabelecimento(current_user: Usuario = Depends(get_current_user)) -> int:
    if not current_user.estabelecimento_id:
        raise HTTPException(status_code=403, detail="Usuário não associado a um estabelecimento")
    
    return current_user.estabelecimento_id