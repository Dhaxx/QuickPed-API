from fastapi import APIRouter, Depends, status
from app.schemas.produto import ProdutoCreate, ProdutoRead, ProdutoUpdate
from app.services.produto import produto_service
from app.auth.dependencies import get_current_estabelecimento
from app.database.engine import get_session

router = APIRouter()

# Rotas dos Produtos
@router.post("/", response_model=ProdutoCreate, status_code=status.HTTP_201_CREATED)
def create_produto(data: ProdutoCreate, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    dados = data.model_dump()
    dados["estabelecimento_id"] = estabelecimento_id
    return produto_service.create(session, dados)

@router.get("/", response_model=list[ProdutoRead], status_code=status.HTTP_200_OK)
def get_produtos( session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento) ):
    return produto_service.get(session, estabelecimento_id)

@router.put("/", response_model=ProdutoRead, status_code=status.HTTP_200_OK)
def update_produto( produto_id: int, data: ProdutoUpdate, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    dados = data.model_dump(exclude_unset=True)
    return produto_service.update(session, produto_id, dados, estabelecimento_id)

@router.delete("/", response_model=ProdutoRead, status_code=status.HTTP_200_OK)
def delete_produto( produto_id: int, session = Depends(get_session), estabelecimento_id: int = Depends(get_current_estabelecimento)):
    return produto_service.delete(session, produto_id, estabelecimento_id)