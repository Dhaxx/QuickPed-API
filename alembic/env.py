from logging.config import fileConfig

from sqlalchemy import pool, create_engine

from alembic import context

from sqlmodel import SQLModel
from app.models.usuario import Usuario
from app.models.estabelecimento import Estabelecimento
from app.models.categoria_produto import CategoriaProduto
from app.models.produto import Produto, GrupoAdicional, Adicional
from app.models.pedido import Pedido
from app.models.comanda import Comanda
from app.models.mesa import Mesa
from app.core.config import settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=settings.db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(settings.db_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
