from sqlmodel import SQLModel, Field
from typing import Optional

class ClienteTokenResponse(SQLModel):
    cliente_id: int
    access_token: str
    token_type: str = "bearer"

class EnderecoCreate(SQLModel):
    cep: Optional[str] = None
    logradouro: str
    numero: str = None
    cidade: str
    bairro: str
    complemento: Optional[str] = None

class EnderecoRead(SQLModel):
    id: int
    cliente_id: int
    logradouro: str
    numero: Optional[str] = None
    cidade: str
    bairro: str
    complemento: Optional[str] = None
    atual: bool

class EnderecoUpdate(SQLModel):
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    cidade: Optional[str] = None
    bairro: Optional[str] = None
    complemento: Optional[str] = None
    atual: Optional[bool] = None

class ClienteCreate(SQLModel):
    nome: str = Field(min_length=2, max_length=50)
    telefone: str = Field(min_length=8, max_length=20, regex=r'^(?:\+55\s?)?(?:\(?\d{2}\)?\s?)?(?:9\d{4}-?\d{4}|\d{4}-?\d{4})$')

class ClienteRead(SQLModel):
    id: int
    nome: str
    telefone: str
    enderecos: Optional[list[EnderecoRead]] = None

class ClienteUpdate(SQLModel):
    nome: Optional[str] = Field(default=None, min_length=2, max_length=50)
    telefone: Optional[str] = Field(default=None, min_length=8, max_length=20, regex=r'^(?:\+55\s?)?(?:\(?\d{2}\)?\s?)?(?:9\d{4}-?\d{4}|\d{4}-?\d{4})$')