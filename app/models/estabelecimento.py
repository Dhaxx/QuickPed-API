from sqlmodel import JSON, Column, Field, SQLModel, Relationship
from typing import Optional, List
from pydantic import EmailStr

def dias_default():
    return [
        {"dia": "Segunda-feira", "abertura": "08:00", "fechamento": "18:00"},
        {"dia": "Terça-feira", "abertura": "08:00", "fechamento": "18:00"},
        {"dia": "Quarta-feira", "abertura": "08:00", "fechamento": "18:00"},
        {"dia": "Quinta-feira", "abertura": "08:00", "fechamento": "18:00"},
        {"dia": "Sexta-feira", "abertura": "08:00", "fechamento": "18:00"},
        {"dia": "Sábado", "abertura": "10:00", "fechamento": "16:00"},
        {"dia": "Domingo", "abertura": "Fechado", "fechamento": "Fechado"}
    ]

class DiaFuncionamento(SQLModel):
    dia: str
    abertura: str
    fechamento: str

class EstabelecimentoBase(SQLModel):
    nome: str
    cnpj: str
    endereco: str
    telefone: str
    email: EmailStr
    logo_url: Optional[str] = None

class Estabelecimento(EstabelecimentoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    dias_funcionamento: List[DiaFuncionamento] = Field(
        sa_column=Column(JSON),
        default_factory=dias_default
    )

    esta_aberto: bool = Field(default=False)
    ativo: bool = Field(default=False)

    categorias: List["CategoriaProduto"] = Relationship(back_populates="estabelecimento")
    usuarios: List["Usuario"] = Relationship( back_populates="estabelecimento" )
    grupos_adicionais: List["GrupoAdicional"] = Relationship( back_populates="estabelecimento" ) 
    adicionais: List["Adicional"] = Relationship( back_populates="estabelecimento" )
    pedidos: List["Pedido"] = Relationship(back_populates="estabelecimento")
    comandas: List["Comanda"] = Relationship(back_populates="estabelecimento")
    mesas: List["Mesa"] = Relationship(back_populates="estabelecimento")