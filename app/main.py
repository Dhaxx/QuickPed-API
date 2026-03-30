from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.engine import create_db_and_tables
from .core.config import settings
from .auth.router import router as autenticacao_router
from .api.v1.admin.estabelecimento import router as estabelecimento_router
from .api.v1.admin.categoria_produto import router as categ_produto_router
from .api.v1.admin.produto import router as produto_router
from .api.v1.admin.grupo_adicional import router as grupo_adicional_router
from .api.v1.admin.adicional import router as adicional_router
from .api.v1.admin.pedido import router as pedido_router
from .api.v1.admin.comanda import router as comanda_router
from .api.v1.admin.mesa import router as mesa_router
from .api.v1.admin.impressao import router as impressao_router
from .api.v1.public.mesa import router as public_mesa_router
from .api.v1.public.cardapio import router as cardapio_router
from .api.v1.public.pedido import router as public_pedido_router
from .api.v1.public.comanda import router as public_comanda_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan, 
    title=settings.app_name, 
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (ajuste conforme necessário)
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os headers
)

# Rotas Administrativas
app.include_router(autenticacao_router, prefix="/api/v1/admin/autenticacao", tags=["Admin - Autenticacao"])
app.include_router(estabelecimento_router, prefix="/api/v1/admin/estabelecimento", tags=["Admin - Estabelecimento"])
app.include_router(categ_produto_router, prefix="/api/v1/admin/categoria-produto", tags=["Admin - Categoria Produto"])
app.include_router(produto_router, prefix="/api/v1/admin/produto", tags=["Admin - Produto"])
app.include_router(grupo_adicional_router, prefix="/api/v1/admin/produto/grupo-adicional", tags=["Admin - Grupo Adicional"])
app.include_router(adicional_router, prefix="/api/v1/admin/produto/adicional", tags=["Admin - Adicional"])
app.include_router(pedido_router, prefix="/api/v1/admin/pedido", tags=["Admin - Pedido"])
app.include_router(comanda_router, prefix="/api/v1/admin/comanda", tags=["Admin - Comanda"])
app.include_router(mesa_router, prefix="/api/v1/admin/mesa", tags=["Admin - Mesa"])
app.include_router(impressao_router, prefix="/api/v1/admin/Impressao", tags=["Admin - Impressao"])

# Rotas Públicas
app.include_router(cardapio_router, prefix="/api/v1/{slug}/cardapio", tags=["Public - Cardápio"])
app.include_router(public_pedido_router, prefix="/api/v1/{slug}/pedido", tags=["Public - Pedido"])
app.include_router(public_mesa_router, prefix="/api/v1/{slug}/mesa", tags=["Public - Mesa"])
app.include_router(public_comanda_router, prefix="/api/v1/{slug}/comanda", tags=["Public - Comanda"])