from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database.engine import create_db_and_tables
from .core.config import settings
from .api.v1.autenticacao import router as autenticacao_router
from .api.v1.estabelecimento import router as estabelecimento_router
from .api.v1.categoria_produto import router as categ_produto_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan, 
    title=settings.app_name, 
)

app.include_router(autenticacao_router, prefix="/api/v1/autenticacao", tags=["autenticacao"])
app.include_router(estabelecimento_router, prefix="/api/v1/estabelecimento", tags=["estabelecimento"])
app.include_router(categ_produto_router, prefix="/api/v1/categoria-produto", tags=["categoria-produto"])