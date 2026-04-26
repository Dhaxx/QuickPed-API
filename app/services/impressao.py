from sqlmodel import Session, select, func
from decimal import Decimal
from app.models.pedido import Pedido
from app.models.produto import Produto, CategoriaProduto
from fastapi import HTTPException


class ImpressaoService:
    def __init__(self):
        # Padrao para 58mm e aprox. 30-32 caracteres
        self.largura_papel = 32

    def formatar_pedido(
        self, session: Session, pedido: dict, detalhado: bool = False
    ) -> str:
        destino_producao = {}

        produto_ids = list({item["produto_id"] for item in pedido.get("itens", [])})

        stmt = (
            select(
                Produto.id,
                Produto.nome,
                Produto.preco,
                func.coalesce(Produto.imprime, CategoriaProduto.imprime).label("imprime_final"),
            )
            .join(CategoriaProduto)
            .where(
                Produto.id.in_(produto_ids),
                func.coalesce(Produto.imprime, CategoriaProduto.imprime) == True
            )
        )
        result = session.exec(stmt).all()

        produto_map = {
            produto_id: {"nome": nome, "preco": preco, "imprime": imprime_final}
            for produto_id, nome, preco, imprime_final in result
        }

        total_pedido = Decimal("0.00")

        for item in pedido.get("itens", []):
            if not produto_map.get(item["produto_id"]):
                continue

            produto_info = produto_map[item["produto_id"]]

            if detalhado:
                valor_unitario = produto_info["preco"]
                total_item = valor_unitario * item.get("quantidade", 1)
                total_pedido += total_item

                adicionais_itens = []
                total_adicionais = Decimal("0.00")
                for adicional in item.get("adicionais", []):
                    if isinstance(adicional, dict):
                        nome_adicional = adicional.get("nome")
                        valor_adicional = adicional.get("preco", Decimal("0.00"))
                    else:
                        nome_adicional = adicional.nome
                        valor_adicional = adicional.preco
                    adicionais_itens.append(
                        {"nome": nome_adicional, "preco": valor_adicional}
                    )
                    total_adicionais += valor_adicional
                    total_pedido += valor_adicional * item.get("quantidade", 1)

                item_formatado = {
                    "produto": item.get("nome_produto"),
                    "quantidade": item.get("quantidade"),
                    "valor_unitario": valor_unitario,
                    "total_item": total_item,
                    "adicionais": adicionais_itens,
                    "total_adicionais": total_adicionais,
                }
            else:
                item_formatado = {
                    "produto": item.get("nome_produto"),
                    "quantidade": item.get("quantidade"),
                    "adicionais": [
                        adicional.get("nome")
                        if isinstance(adicional, dict)
                        else adicional.nome
                        for adicional in item.get("adicionais", [])
                    ],
                }

            destino = item.get("produzido_por") or "GERAL"
            destino_producao.setdefault(destino, []).append(item_formatado)

        linhas = []
        for categoria, itens in destino_producao.items():
            titulo_pedido = f"[Pedido #{pedido.get('id')}]"
            linhas.append(titulo_pedido.center(self.largura_papel, "="))

            linhas.append(f"Preparador: {categoria.upper()}")
            linhas.append(f"Mesa: {pedido.get('numero_mesa')}")
            linhas.append(f"Cliente: {pedido.get('nome_cliente')}")
            linhas.append(
                f"Data: {pedido.get('criado_em').strftime('%d/%m/%Y %H:%M:%S')}"
            )

            titulo_itens = "[Itens]"
            linhas.append(titulo_itens.center(self.largura_papel, "="))

            for item in itens:
                if detalhado:
                    linhas.append(f"{item['quantidade']}x {item['produto']}")
                    linhas.append(f"  R$ {item['valor_unitario']:.2f} cada")
                    linhas.append(f"  Subtotal: R$ {item['total_item']:.2f}")
                    if item["adicionais"]:
                        for adicional in item["adicionais"]:
                            linhas.append(
                                f"  + {adicional['nome']} (R$ {adicional['preco']:.2f})"
                            )
                        linhas.append(
                            f"  Adicionais: R$ {item['total_adicionais']:.2f}"
                        )
                else:
                    linhas.append(f"{item['quantidade']}x {item['produto']}")
                    if item["adicionais"]:
                        for adicional in item["adicionais"]:
                            linhas.append(f"  + {adicional}")

            if detalhado:
                linhas.append(f"TOTAL PEDIDO: R$ {total_pedido:.2f}")

            linhas.append("=" * self.largura_papel)
            linhas.append("\n")  # Espaço entre categorias

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

    def formatar_comanda(
        self, session: Session, comanda: "Comanda", pedidos: list[Pedido]
    ) -> str:
        from app.models.comanda import Comanda
        from decimal import Decimal

        linhas = []
        linhas.append(f"[Comanda #{comanda.id}]".center(self.largura_papel, "="))
        linhas.append(f"Mesa: {comanda.numero_mesa}")
        linhas.append(f"Status: {comanda.status.value.upper()}")
        linhas.append("=" * self.largura_papel)

        produto_ids = set()
        itens_por_produto = {}

        for pedido in pedidos:
            for item in pedido.itens:
                produto_id = (
                    item.get("produto_id")
                    if isinstance(item, dict)
                    else item.produto_id
                )
                produto_ids.add(produto_id)

                nome_produto = (
                    item.get("nome_produto")
                    if isinstance(item, dict)
                    else item.nome_produto
                )
                preco_unitario = (
                    item.get("preco_unitario")
                    if isinstance(item, dict)
                    else item.preco_unitario
                )
                quantidade = (
                    item.get("quantidade")
                    if isinstance(item, dict)
                    else item.quantidade
                )
                adicionais = (
                    item.get("adicionais", [])
                    if isinstance(item, dict)
                    else item.adicionais
                )

                nomes_adicionais = frozenset(
                    adj.get("nome") if isinstance(adj, dict) else adj.nome
                    for adj in adicionais
                )
                key = (produto_id, nomes_adicionais)

                if key not in itens_por_produto:
                    itens_por_produto[key] = {
                        "nome_produto": nome_produto,
                        "quantidade": 0,
                        "preco_unitario": preco_unitario,
                        "adicionais": [],
                    }
                itens_por_produto[key]["quantidade"] += quantidade
                itens_por_produto[key]["adicionais"].extend(adicionais)

        stmt = select(Produto.nome, Produto.preco).where(Produto.id.in_(produto_ids))
        precos_db = {row[0]: row[1] for row in session.exec(stmt).all()}

        linhas.append(f"{'Produto':<12} {'Uni.':>8} {'Total':>9}")
        linhas.append("-" * self.largura_papel)

        total_comanda = Decimal("0.00")

        for produto_id, item_data in itens_por_produto.items():
            nome = item_data["nome_produto"][:15]
            preco_unitario = Decimal(str(item_data["preco_unitario"]))
            quantidade = item_data["quantidade"]
            total_item = preco_unitario * quantidade

            total_adicionais = Decimal("0.00")
            linhas_adicionais = []
            for adicional in item_data["adicionais"]:
                if isinstance(adicional, dict):
                    nome_adj = adicional.get("nome", "")
                    preco_adj = Decimal(str(adicional.get("preco", "0.00")))
                else:
                    nome_adj = adicional.nome
                    preco_adj = Decimal(str(adicional.preco))
                linhas_adicionais.append(f"  + {nome_adj}  {preco_adj:.2f}")
                total_adicionais += preco_adj

            total_item_completo = total_item + (total_adicionais * quantidade)
            total_comanda += total_item_completo

            linhas.append( f"{quantidade}x {nome:<12}{preco_unitario:>8.2f}{total_item_completo:>9.2f}" )
            for la in linhas_adicionais:
                linhas.append(la)

        linhas.append("=" * self.largura_papel)
        linhas.append(f"TOTAL: R$ {total_comanda:.2f}".center(self.largura_papel))
        linhas.append("=" * self.largura_papel)

        return "\n".join(linhas)

    def imprimir_comanda(
        self, session: Session, comanda_id: int, estabelecimento_id: int
    ) -> dict:
        from app.models.comanda import Comanda

        comanda = session.exec(
            select(Comanda).where(
                Comanda.id == comanda_id,
                Comanda.estabelecimento_id == estabelecimento_id,
            )
        ).first()

        if not comanda:
            raise HTTPException(status_code=404, detail="Comanda não encontrada")

        pedidos = session.exec(
            select(Pedido).where(
                Pedido.comanda_id == comanda_id,
                Pedido.estabelecimento_id == estabelecimento_id,
                Pedido.oculto == False,
            )
        ).all()

        if not pedidos:
            raise HTTPException(
                status_code=404, detail="Nenhum pedido encontrado para esta comanda"
            )

        texto_formatado = self.formatar_comanda(session, comanda, pedidos)
        print(texto_formatado)

        return {"comanda_id": comanda_id, "texto": texto_formatado}


impressao_service = ImpressaoService()
