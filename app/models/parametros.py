from sqlmodel import Field, SQLModel, Relationship

class ParametrosBase(SQLModel):
    estabelecimento_id: int = Field(index=True, foreign_key="estabelecimento.id", nullable=False, primary_key=True)
    auto_atendimento: bool = Field(default=False)
    delivery: bool = Field(default=False)

class Parametros(ParametrosBase, table=True):
    estabelecimento: "Estabelecimento" = Relationship(back_populates="parametros")