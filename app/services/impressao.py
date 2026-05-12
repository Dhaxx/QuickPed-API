from sqlmodel import Session, select, func, text
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
        self, session: Session, comanda: list[tuple]
    ) -> str:
        from decimal import Decimal

        linhas = []

        linhas.append(f"[Comanda #{comanda[0].comanda_id}]".center(self.largura_papel, "="))
        linhas.append(f"Mesa: {comanda[0].numero_mesa}")
        linhas.append(f"Status: {comanda[0].status}")
        linhas.append("=" * self.largura_papel)

        linhas.append(f"{'Produto':<12} {'Uni.':>8} {'Total':>9}")
        linhas.append("-" * self.largura_papel)
        total_comanda = Decimal("0.00")

        for row in comanda:
            linhas.append(
                f"{int(row.quantidade)}x "
                f"{row.nome_produto[:12]:<12}"
                f"{Decimal(row.preco_unitario):>8.2f}"
                f"{Decimal(row.total_item):>9.2f}"
            )

            if row.adicionais:
                for adicional in row.adicionais:
                    if adicional[0] == None:
                        continue

                    linhas.append(
                        f"  + {adicional[0]} "
                        f"{Decimal(adicional[1]):.2f}"
                    )

            total_comanda += Decimal(row.total_item)

        linhas.append("=" * self.largura_papel)
        linhas.append(
            f"TOTAL: R$ {total_comanda:.2f}".center(
                self.largura_papel
            )
        )
        linhas.append("=" * self.largura_papel)

        return "\n".join(linhas)

    def imprimir_comanda(
        self, session: Session, comanda_id: int, estabelecimento_id: int
    ) -> dict:
        stmt = """
        with itens_comanda as (
        select
            comanda_id,
            numero_mesa,
            concat(p.id,'.',item->>'item_id'::text) item_id,
            item->>'nome_produto' as nome_produto,
            adicional->>'nome' adicional,
            (item->>'preco_unitario')::numeric preco_unitario,
            coalesce((adicional->>'preco'), '0')::numeric preco_unitario_add,
            (item->>'quantidade')::numeric quantidade
        from
            pedido p
        cross join lateral jsonb_array_elements(itens::jsonb) as item
        left join lateral jsonb_array_elements(item->'adicionais') as adicional on
            true
        where
            comanda_id = :id
            and p.estabelecimento_id = :estabelecimento_id)
        select
            comanda_id,
            c.status,
            numero_mesa,
            item_id,
            nome_produto,
            jsonb_agg( jsonb_build_array( adicional, preco_unitario_add ) ) AS adicionais,
            quantidade,
            preco_unitario,
            (ic.preco_unitario + sum(ic.preco_unitario_add)) * ic.quantidade total_item
        from
            itens_comanda ic
        join (
            select
                id comanda_id,
                status
            from
                comanda) c
                using (comanda_id)
        group by comanda_id,
            c.status,
            numero_mesa,
            item_id,
            nome_produto,
            preco_unitario,
            quantidade
        """

        rows = session.exec( text(stmt), params={"id": comanda_id} ).all()

        if not rows:
            raise HTTPException(status_code=500, detail="Erro ao gerar comanda: sem itens encontrados")

        texto_formatado = self.formatar_comanda(session, rows)
        print(texto_formatado)

        return {"comanda_id": comanda_id, "texto": texto_formatado}


impressao_service = ImpressaoService()
