from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database.engine import create_db_and_tables
from .core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan, 
    title=settings.app_name, 
)
