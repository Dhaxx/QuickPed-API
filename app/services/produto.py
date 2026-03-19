from app.models.produto import Produto, GrupoAdicional, Adicional
from app.services.base import BaseService

class ProdutoService(BaseService[Produto]):
    pass

class GrupoAdicionalService(BaseService[GrupoAdicional]):
    pass

class AdicionalService(BaseService[Adicional]):
    pass

produto_service = ProdutoService(Produto)
grupo_adicional_service = GrupoAdicionalService(GrupoAdicional)
adicional_service = AdicionalService(Adicional)