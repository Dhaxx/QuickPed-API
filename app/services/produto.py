from app.models.produto import Produto, GrupoAdicional, Adicional
from app.services.base import BaseService

class ProdutoService(BaseService[Produto]):
    pass

class GrupoAdicionalService(BaseService[GrupoAdicional]):
    def get(self, session, estabelecimento_id, produto_id):
        return session.query(self.model).filter_by(estabelecimento_id=estabelecimento_id, produto_id=produto_id).all()

class AdicionalService(BaseService[Adicional]):
    def get(self, session, estabelecimento_id, grupo_id):
        return session.query(self.model).filter_by(estabelecimento_id=estabelecimento_id, grupo_id=grupo_id).all()

produto_service = ProdutoService(Produto)
grupo_adicional_service = GrupoAdicionalService(GrupoAdicional)
adicional_service = AdicionalService(Adicional)