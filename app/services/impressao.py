from sqlmodel import Session, select
from app.models.pedido import Pedido
from fastapi import HTTPException
from datetime import datetime


class ImpressaoService:
    def formatar_pedido(self, pedido: dict) -> str:
        destino_producao = {}

        for item in pedido.get("itens", []):
            destino = item.get("produzido_por") or "GERAL"

            destino_producao.setdefault(destino, []).append(
                {
                    "produto": item.get("nome_produto"),
                    "quantidade": item.get("quantidade"),
                    "adicionais": [
                        adicional.get("nome")
                        if isinstance(adicional, dict)
                        else adicional.nome
                        for adicional in item.get("adicionais", [])
                    ],
                }
            )

        linhas = []

        for categoria, itens in destino_producao.items():
            linhas.append(f"{'=' * 20}[Pedido #{pedido.get('id')}]{'=' * 20}")
            linhas.append(f"Preparador: {categoria.upper()}")
            linhas.append(f"N° Mesa: {pedido.get('numero_mesa')}")
            linhas.append(f"Cliente: {pedido.get('nome_cliente')}")
            linhas.append(f"{'=' * 23}[Itens]{'=' * 22}")

            for item in itens:
                linhas.append(f"- {item['quantidade']}x {item['produto']}")

                if item["adicionais"]:
                    for adicional in item["adicionais"]:
                        linhas.append(f"   + {adicional}")

            linhas.append(f"{'=' * 52}\n\n")

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
