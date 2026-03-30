from sqlmodel import Session, select
from app.models.pedido import Pedido
from fastapi import HTTPException

class ImpressaoService:
    def imprimir_pedido(self, session: Session, pedido_id: int, estabelecimento_id: int) -> None:
        pedido = session.exec(
            select(Pedido).where(
                Pedido.id == pedido_id,
                Pedido.estabelecimento_id == estabelecimento_id
            )
        ).first()

        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        destino_producao = {}

        for item in pedido.itens:
            destino = item.get('produzido_por') or "GERAL"

            destino_producao.setdefault(destino, []).append({
                "produto": item.get('nome_produto'),
                "quantidade": item.get('quantidade'),
                "adicionais": [
                    adicional.get('nome') if isinstance(adicional, dict) else adicional.nome
                    for adicional in item.get('adicionais', [])
                ]
            })

        # 🔥 imprime uma comanda por categoria
        for categoria, itens in destino_producao.items():

            linhas = []
            linhas.append(f"{20*'═'}[Pedido #{pedido.id}]{20*'═'}")
            linhas.append(f"Preparador: {categoria.upper()}")
            linhas.append(f"N° Mesa: {pedido.numero_mesa}")
            linhas.append(f"Cliente: {pedido.nome_cliente}")
            linhas.append(f"{23*'═'}[Itens]{22*'═'}")

            for item in itens:
                linhas.append(f"- {item['quantidade']}x {item['produto']}")

                if item["adicionais"]:
                    for adicional in item["adicionais"]:
                        linhas.append(f"   + {adicional}")

            linhas.append(f"{52*'═'}\n\n\n")

            texto_final = "\n".join(linhas)

            print(texto_final)

impressao_service = ImpressaoService()