from sqlmodel import SQLModel, create_engine, Session
from ..core.config import settings
from ..models.estabelecimento import Estabelecimento
from ..models.categoria_produto import CategoriaProduto
from ..models.produto import Produto
from ..models.pedido import Pedido

engine = create_engine(settings.db_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session