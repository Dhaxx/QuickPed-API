from fastapi import APIRouter, Depends, status
from app.schemas.categoria_produto import CategoriaProdutoCreate, CategoriaProdutoRead, CategoriaProdutoUpdate
from app.services.categoria_produto import categoria_produto_service
from app.database.engine import get_session
from app.auth.dependencies import get_current_user, get_current_estabelecimento

router = APIRouter()

@router.post("/", response_model=CategoriaProdutoRead, status_code=status.HTTP_201_CREATED)
def create_categoria_produto(
    data: CategoriaProdutoCreate,
    session = Depends(get_session),
    estabelecimento_id: int = Depends(get_current_estabelecimento)
):
    dados = data.model_dump()

    dados["estabelecimento_id"] = estabelecimento_id

    return categoria_produto_service.create(session, dados)

@router.get("/", response_model=list[CategoriaProdutoRead], status_code=status.HTTP_200_OK)
def get_categoria_produtos(
    session = Depends(get_session),
    estabelecimento_id: int = Depends(get_current_estabelecimento)
):
    return categoria_produto_service.get(session, estabelecimento_id)

@router.put("/", response_model=CategoriaProdutoRead, status_code=status.HTTP_200_OK)
def update_categoria_produto(
    categoria_produto_id: int,
    data: CategoriaProdutoUpdate,
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    session = Depends(get_session)
):
    dados = data.model_dump(exclude_unset=True)
    return categoria_produto_service.update(session, categoria_produto_id, dados, estabelecimento_id)

@router.delete("/{categoria_produto_id}", response_model=CategoriaProdutoRead, status_code=status.HTTP_200_OK)
def delete_categoria_produto(
    categoria_produto_id: int,
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    session = Depends(get_session)
):
    return categoria_produto_service.delete(session, categoria_produto_id, estabelecimento_id)