from sqlmodel import SQLModel, create_engine, Session, select
from ..core.config import settings
from ..models.estabelecimento import Estabelecimento
from ..models.categoria_produto import CategoriaProduto
from ..models.produto import Produto, GrupoAdicional, Adicional
from ..models.pedido import Pedido
from ..models.comanda import Comanda
from ..models.usuario import Usuario
from ..auth.hash import gerar_hash

if settings.sgbd_driver == "sqlite":
    engine = create_engine(settings.db_url, echo=True)
else:
    engine = create_engine(
        settings.db_url,
        echo=True,
        pool_size=20,
        max_overflow=40,
        pool_pre_ping=True,
        pool_recycle=3600,
    )


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_system_establishment():
    with Session(engine) as session:
        stmt_estab = select(Estabelecimento).where(
            Estabelecimento.cnpj == "00000000000000"
        )
        estabelecimento = session.exec(stmt_estab).first()

        if not estabelecimento:
            estabelecimento = Estabelecimento(
                nome="Teste",
                cnpj="00000000000000",
                endereco="",
                telefone="",
                email="teste@quickped.com",
                ativo=True,
                slug="teste",
            )
            session.add(estabelecimento)
            session.commit()
            session.refresh(estabelecimento)

def create_master_user():
    with Session(engine) as session:
        stmt = select(Usuario).where(
            Usuario.usuario == settings.db_user, Usuario.master == True
        )
        existing = session.exec(stmt).first()

        if existing:
            return

        stmt_estab = select(Estabelecimento).where(
            Estabelecimento.cnpj == "00000000000000"
        )
        estabelecimento = session.exec(stmt_estab).first()

        user = Usuario(
            usuario=settings.db_user,
            senha_hash=gerar_hash(settings.db_password),
            estabelecimento_id=estabelecimento.id,  # type: ignore[arg-type]
            admin=True,
            master=True,
        )
        session.add(user)
        session.commit()


def get_session():
    with Session(engine) as session:
        yield session
