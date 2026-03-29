from app.models.produto import Produto, GrupoAdicional, Adicional
from app.services.base import BaseService
from sqlalchemy.orm import Session

class ProdutoService(BaseService[Produto]):
    pass

class GrupoAdicionalService(BaseService[GrupoAdicional]):
    def get(self, session, estabelecimento_id, produto_id):
        return session.query(self.model).filter_by(estabelecimento_id=estabelecimento_id, produto_id=produto_id).all()
    
    def create(self, session: Session, estabelecimento_id: int, data) -> GrupoAdicional:
        grupo = GrupoAdicional(
            nome=data.nome,
            max_selecoes=data.max_selecoes,
            produto_id=data.produto_id,
            estabelecimento_id=estabelecimento_id
        )
        session.add(grupo)
        session.commit()
        session.refresh(grupo)

        print(f'\n\n{data.adicionais}\n\n')

        if data.adicionais:
            for adicional_data in data.adicionais:
                adicional = Adicional(
                    nome=adicional_data.nome,
                    preco=adicional_data.preco,
                    grupo_id=grupo.id,
                    estabelecimento_id=estabelecimento_id
                )
                session.add(adicional)
            session.commit()

        return grupo


class AdicionalService(BaseService[Adicional]):
    def get(self, session, estabelecimento_id, grupo_id):
        return session.query(self.model).filter_by(estabelecimento_id=estabelecimento_id, grupo_id=grupo_id).all()

produto_service = ProdutoService(Produto)
grupo_adicional_service = GrupoAdicionalService(GrupoAdicional)
adicional_service = AdicionalService(Adicional)