from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database.engine import create_db_and_tables
from .core.config import settings
from .auth.router import router as autenticacao_router
from .api.v1.estabelecimento import router as estabelecimento_router
from .api.v1.categoria_produto import router as categ_produto_router
from .api.v1.produto import router as produto_router
from .api.v1.grupo_adicional import router as grupo_adicional_router
from .api.v1.adicional import router as adicional_router
from .api.v1.pedido import router as pedido_router
from .api.v1.comanda import router as comanda_router
from .api.v1.mesa import router as mesa_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan, 
    title=settings.app_name, 
)

# Rotas Administrativas
app.include_router(autenticacao_router, prefix="/api/v1/admin/autenticacao", tags=["Autenticacao"])
app.include_router(estabelecimento_router, prefix="/api/v1/admin/estabelecimento", tags=["Estabelecimento"])
app.include_router(categ_produto_router, prefix="/api/v1/admin/categoria-produto", tags=["Categoria Produto"])
app.include_router(produto_router, prefix="/api/v1/admin/produto", tags=["Produto"])
app.include_router(grupo_adicional_router, prefix="/api/v1/admin/produto/grupo-adicional", tags=["Grupo Adicional"])
app.include_router(adicional_router, prefix="/api/v1/admin/produto/adicional", tags=["Adicional"])
app.include_router(pedido_router, prefix="/api/v1/admin/pedido", tags=["Pedido"])
app.include_router(comanda_router, prefix="/api/v1/admin/comanda", tags=["Comanda"])
app.include_router(mesa_router, prefix="/api/v1/admin/mesa", tags=["Mesa"])