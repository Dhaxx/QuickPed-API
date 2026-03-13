from ...models.estabelecimento import Estabelecimento
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/estabelecimento", tags=["estabelecimento"])

@router.post("/", response_model=Estabelecimento)
async def criar_estabelecimento(estabelecimento: Estabelecimento):
    # Lógica para criar um estabelecimento
    return {}