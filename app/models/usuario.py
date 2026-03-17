from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class UsuarioBase(SQLModel):
    usuario: str
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id", index=True) 

class Usuario(UsuarioBase, table=True):
    id: int = Field(default=None, primary_key=True)
    senha_hash: str
    ativo: bool = Field(default=True)
    criado_em: datetime = Field(default_factory=lambda: datetime.now())
    estabelecimento: "Estabelecimento" = Relationship(back_populates="usuarios")
