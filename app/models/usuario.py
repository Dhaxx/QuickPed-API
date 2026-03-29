from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone

class UsuarioBase(SQLModel):
    usuario: str
    estabelecimento_id: int = Field(foreign_key="estabelecimento.id", index=True) 

class Usuario(UsuarioBase, table=True):
    id: int = Field(default=None, primary_key=True)
    senha_hash: str
    ativo: bool = Field(default=True)
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    admin: bool = Field(default=False)  

    estabelecimento: "Estabelecimento" = Relationship(back_populates="usuarios")
    produtos: list["Produto"] = Relationship(back_populates="produzido_por_usuario")
    categorias: list["CategoriaProduto"] = Relationship(back_populates="produzido_por_usuario")
