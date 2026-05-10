from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from app.core.config import settings

class PermissoesEnum(str, Enum):
    EDITAR = "editar"
    VISUALIZAR = "visualizar"
    BLOQUEADO = "bloqueado"


class PermissaoUsuario(SQLModel, table=True):
    __tablename__ = "permissoes_usuario"

    id: int = Field(primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    dashboard: PermissoesEnum = Field(default=PermissoesEnum.BLOQUEADO)
    pedidos: PermissoesEnum = Field(default=PermissoesEnum.BLOQUEADO)
    comandas: PermissoesEnum = Field(default=PermissoesEnum.BLOQUEADO)
    produtos: PermissoesEnum = Field(default=PermissoesEnum.BLOQUEADO)
    mesas: PermissoesEnum = Field(default=PermissoesEnum.BLOQUEADO)
    estabelecimento: PermissoesEnum = Field(default=PermissoesEnum.BLOQUEADO)
    usuarios: PermissoesEnum = Field(default=PermissoesEnum.BLOQUEADO)
    atualizado_em: datetime = Field(default_factory=settings.time_now)
    
    usuario: "Usuario" = Relationship(back_populates="permissoes")
