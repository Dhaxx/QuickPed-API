from sqlmodel import SQLModel, Field, Relationship, DateTime
from datetime import datetime

class UsuarioBase(SQLModel):
    login: str
    senha_hash: str
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id", index=True)
    ativo: bool = Field(default=True)
    criado_em: DateTime = Field(default_factory=lambda: datetime.utcnow())

class Usuario(UsuarioBase, table=True):
    id: int = Field(default=None, primary_key=True)
    estabelecimento: "Estabelecimento" = Relationship(back_populates="usuarios")