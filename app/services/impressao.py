from sqlmodel import Session, select, func
from app.models.pedido import Pedido
from app.models.produto import Produto, CategoriaProduto
from fastapi import HTTPException

class ImpressaoService:
    def __init__(self):
        # Padrao para 58mm e aprox. 30-32 caracteres
        self.largura_papel = 32 

    def formatar_pedido(self, session: Session, pedido: dict) -> str:
        destino_producao = {}

        produto_ids = list({
            item["produto_id"]
            for item in pedido.get("itens", [])
        })

        stmt = (
            select(
                Produto.id,
                func.coalesce(Produto.imprime, CategoriaProduto.imprime).label("imprime_final")
            )
            .join(CategoriaProduto)
            .where(Produto.id.in_(produto_ids))
        )
        result = session.exec(stmt).all()

        imprime_map = {
            produto_id: imprime_final
            for produto_id, imprime_final in result
        }

        for item in pedido.get("itens", []):
            if not imprime_map.get(item["produto_id"]):
                continue

            destino = item.get("produzido_por") or "GERAL"
            destino_producao.setdefault(destino, []).append({
                "produto": item.get("nome_produto"),
                "quantidade": item.get("quantidade"),
                "adicionais": [
                    adicional.get("nome") if isinstance(adicional, dict) else adicional.nome
                    for adicional in item.get("adicionais", [])
                ],
            })

        linhas = []
        for categoria, itens in destino_producao.items():
            # Centralizando [Pedido #ID] com preenchimento de '='
            titulo_pedido = f"[Pedido #{pedido.get('id')}]"
            linhas.append(titulo_pedido.center(self.largura_papel, "="))
            
            linhas.append(f"Preparador: {categoria.upper()}")
            linhas.append(f"Mesa: {pedido.get('numero_mesa')}")
            linhas.append(f"Cliente: {pedido.get('nome_cliente')}")
            linhas.append(f"Data: {pedido.get('criado_em').strftime('%d/%m/%Y %H:%M:%S')}")
            
            # Centralizando [Itens] com preenchimento de '='
            titulo_itens = "[Itens]"
            linhas.append(titulo_itens.center(self.largura_papel, "="))

            for item in itens:
                linhas.append(f"{item['quantidade']}x {item['produto']}")
                if item["adicionais"]:
                    for adicional in item["adicionais"]:
                        linhas.append(f"  + {adicional}")

            # Linha final de fechamento
            linhas.append("=" * self.largura_papel)
            linhas.append("\n") # Espaço entre categorias

        return "\n".join(linhas)

    def imprimir_pedido(
        self, session: Session, pedido_id: int, estabelecimento_id: int
    ) -> dict:
        pedido = session.exec(
            select(Pedido).where(
                Pedido.id == pedido_id, Pedido.estabelecimento_id == estabelecimento_id
            )
        ).first()

        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        pedido_dict = {
            "id": pedido.id,
            "numero_mesa": pedido.numero_mesa,
            "nome_cliente": pedido.nome_cliente,
            "itens": pedido.itens,
            "criado_em": pedido.criado_em,
        }

        texto_formatado = self.formatar_pedido(session, pedido_dict)

        print(texto_formatado)

        return {"pedido_id": pedido_id, "texto": texto_formatado}


impressao_service = ImpressaoService()
