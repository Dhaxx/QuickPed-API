from sqlmodel import Session, select
from app.models.pedido import Pedido
from fastapi import HTTPException

class ImpressaoService:
    def __init__(self):
        # Padrao para 58mm e aprox. 30-32 caracteres
        self.largura_papel = 32 

    def formatar_pedido(self, pedido: dict) -> str:
        destino_producao = {}

        for item in pedido.get("itens", []):
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
        }

        texto_formatado = self.formatar_pedido(pedido_dict)

        print(texto_formatado)

        return {"pedido_id": pedido_id, "texto": texto_formatado}


impressao_service = ImpressaoService()
