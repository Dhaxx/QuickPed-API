from fastapi import APIRouter, Depends, HTTPException, status
from app.models.estabelecimento import Estabelecimento
from app.schemas.cardapio import CardapioPublicResponse
from app.services.cardapio import CardapioService
from app.database.engine import get_session
from sqlmodel import Session, select

router = APIRouter()


@router.get("/", response_model=CardapioPublicResponse, status_code=status.HTTP_200_OK)
def get_cardapio(session: Session = Depends(get_session), slug: str = None):
    stmt = select(Estabelecimento).where(Estabelecimento.slug == slug)
    estabelecimento = session.exec(stmt).first()

    if not estabelecimento:
        return {"message": "Estabelecimento não encontrado"}

    if not estabelecimento.ativo:
        raise HTTPException(status_code=404, detail="Estabelecimento inativo")

    return CardapioService.obter_cardapio(session, estabelecimento.id)
