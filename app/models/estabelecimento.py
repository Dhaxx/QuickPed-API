from sqlmodel import JSON, Column, Field, SQLModel
from typing import Optional, List, Dict

class Estabelecimento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    cnpj: str
    endereco: str
    telefone: str
    email: str
    dias_funcionamento: List[Dict] = Field(sa_column=Column(JSON), default=[
        {"dia": "Segunda-feira", "abertura": "08:00", "fechamento": "18:00"},
        {"dia": "Terça-feira", "abertura": "08:00", "fechamento": "18:00"},
        {"dia": "Quarta-feira", "abertura": "08:00", "fechamento": "18:00"},
        {"dia": "Quinta-feira", "abertura": "08:00", "fechamento": "18:00"},
        {"dia": "Sexta-feira", "abertura": "08:00", "fechamento": "18:00"},
        {"dia": "Sábado", "abertura": "10:00", "fechamento": "16:00"},
        {"dia": "Domingo", "abertura": "Fechado", "fechamento": "Fechado"}
    ])
    logo_url: Optional[str] = None
    esta_aberto: bool = Field(default=False)
    ativo: bool = Field(default=False)