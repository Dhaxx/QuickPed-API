from fastapi import APIRouter, Depends, status
from app.models.estabelecimento import Estabelecimento
from app.schemas.cardapio import CardapioPublicResponse
from app.services.cardapio import CardapioService
from app.database.engine import get_session
from sqlmodel import Session, select

router = APIRouter()

@router.get("/{slug_estabelecimento}", response_model=CardapioPublicResponse, status_code=status.HTTP_200_OK)
def get_cardapio(session: Session = Depends(get_session), slug_estabelecimento: str = None):
    stmt = select(Estabelecimento.id).where(Estabelecimento.slug == slug_estabelecimento)
    estabelecimento_id = session.exec(stmt).first()


    if not estabelecimento_id:
        return {"message": "Estabelecimento não encontrado"}

    return CardapioService.obter_cardapio(session, estabelecimento_id)