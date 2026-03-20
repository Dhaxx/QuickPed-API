from sqlmodel import Session, text
import json
from app.schemas.cardapio import CardapioPublicResponse, CategoriaPublic, ProdutoPublic, AdicionalPublic

SQL_CARDAPIO_JSON = """
select
    cp.id as categoria_id,
    cp.nome as nome_categoria,
    cp.ordem as ordem_categoria,
    p.id as produto_id,
    p.nome as nome_produto,
    p.descricao,
    p.preco as preco_produto,
    coalesce(
        json_agg(
            json_build_object(
                'id', a.id,
                'nome', a.nome,
                'preco', a.preco
            )
        ) filter (where a.id is not null), '[]'
    ) as adicionais
from categoria_produto cp
join produto p on p.categoria_id = cp.id and p.ativo = true and cp.ativo = true
left join grupo_adicional ga on ga.produto_id = p.id
left join adicional a on a.grupo_id = ga.id
where cp.estabelecimento_id = :estabelecimento_id
group by cp.id, cp.nome, cp.ordem, p.id, p.nome, p.descricao, p.preco
order by cp.ordem, cp.nome, p.nome
"""

class CardapioService:
    @staticmethod
    def obter_cardapio(session: Session, estabelecimento_id: int) -> CardapioPublicResponse:
        rows = session.exec(
            text(SQL_CARDAPIO_JSON), 
            params={"estabelecimento_id": estabelecimento_id}
        ).all()

        categorias_dict = {}

        for r in rows:
            # Categoria
            cat_id = r.categoria_id
            if cat_id not in categorias_dict:
                categorias_dict[cat_id] = {
                    "id": cat_id,
                    "nome": r.nome_categoria,
                    "ordem": r.ordem_categoria,
                    "produtos": []
                }

            # Produto
            produto = ProdutoPublic(
                id=r.produto_id,
                nome=r.nome_produto,
                descricao=r.descricao,
                preco=r.preco_produto,
                disponivel=True,
                adicionais=[AdicionalPublic(**a) for a in json.loads(r.adicionais)]
            )

            categorias_dict[cat_id]["produtos"].append(produto)

        # Transformar dict em lista
        categorias_list = [CategoriaPublic(**cat) for cat in categorias_dict.values()]

        return CardapioPublicResponse(categorias=categorias_list)