from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 60 * 24  # 1 dia

def criar_token(data: dict):
    """
    Gera um token JWT com os dados fornecidos.

    Args:
        data (dict): Dados a serem incluídos no payload do token.

    Returns:
        str: Token JWT codificado.

    O token gerado inclui uma data de expiração ('exp') definida para alguns minutos à frente, conforme especificado pela constante EXPIRATION_MINUTES. O token é assinado usando a chave secreta (SECRET_KEY) e o algoritmo especificado (ALGORITHM).
    """
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    payload.update({"exp": expire})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token