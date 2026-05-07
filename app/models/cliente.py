from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(min_length=2, max_length=50)
    telefone: str = Field(min_length=8, max_length=15, index=True)

    enderecos: List["Endereco"] = Relationship(back_populates="cliente")

class Endereco(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id", index=True)
    logradouro: str = Field(min_length=10, max_length=100)
    numero: Optional[str] = Field(default=None, max_length=20)
    cidade: str = Field(min_length=2, max_length=50)
    bairro: str = Field(min_length=2, max_length=50)
    complemento: Optional[str] = None
    atual: bool = Field(default=False, index=True)

    cliente: "Cliente" = Relationship(back_populates="enderecos")
    pedidos_delivery: List["Pedido"] = Relationship(back_populates="delivery_endereco")