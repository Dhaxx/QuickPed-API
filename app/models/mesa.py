from sqlmodel import SQLModel, Field, UniqueConstraint, Relationship
from typing import Optional
import uuid
from datetime import datetime

class MesaBase(SQLModel):
    numero: int = Field(index=True, nullable=False)

class Mesa(MesaBase, table=True):
    __table_args__ = (
        UniqueConstraint("estabelecimento_id", "numero", name="uq_mesa_estabelecimento_numero"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    estabelecimento_id: int = Field(index=True)

    token: str = Field(default_factory=lambda: str(uuid.uuid4()), unique=True, index=True)

    ativa: bool = Field(default=True)

    criado_em: Optional[datetime] = None

    estabelecimento: "Estabelecimento" = Relationship(back_populates="mesas")