from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database.engine import create_db_and_tables
from .core.config import settings
from .api.v1.estabelecimento import router as estabelecimento_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan, 
    title=settings.app_name, 
)

app.include_router(estabelecimento_router, prefix="/api/v1/estabelecimento", tags=["estabelecimento"])