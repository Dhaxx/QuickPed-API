from app.models.categoria_produto import CategoriaProduto
from app.services.base import BaseService
from sqlmodel import Session

class CategoriaProdutoService(BaseService[CategoriaProduto]):
    pass

categoria_produto_service = CategoriaProdutoService(CategoriaProduto)