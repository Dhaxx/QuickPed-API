"""add_cliente__endereco__tipo_pedido

Revision ID: 7c96fd3fae57
Revises: b90dd71a68dd
Create Date: 2026-05-07 23:12:40.466136
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7c96fd3fae57"
down_revision: Union[str, Sequence[str], None] = "b90dd71a68dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


tipo_pedido_enum = sa.Enum(
    "LOCAL",
    "DELIVERY",
    "RETIRADA",
    name="tipopedido",
)


def upgrade() -> None:
    """Upgrade schema."""

    # =========================================================
    # ENUM
    # =========================================================

    tipo_pedido_enum.create(op.get_bind(), checkfirst=True)

    # =========================================================
    # TABELA CLIENTE
    # =========================================================

    op.create_table(
        "cliente",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=50), nullable=False),
        sa.Column("telefone", sa.String(length=15), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_cliente_telefone"),
        "cliente",
        ["telefone"],
        unique=False,
    )

    # =========================================================
    # TABELA ENDERECO
    # =========================================================

    op.create_table(
        "endereco",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cliente_id", sa.Integer(), nullable=False),
        sa.Column("logradouro", sa.String(length=100), nullable=False),
        sa.Column("numero", sa.String(length=20), nullable=True),
        sa.Column("cidade", sa.String(length=50), nullable=False),
        sa.Column("bairro", sa.String(length=50), nullable=False),
        sa.Column("complemento", sa.String(), nullable=True),
        sa.Column("atual", sa.Boolean(), nullable=False),

        sa.ForeignKeyConstraint(
            ["cliente_id"],
            ["cliente.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_endereco_cliente_id"),
        "endereco",
        ["cliente_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_endereco_atual"),
        "endereco",
        ["atual"],
        unique=False,
    )

    # =========================================================
    # ALTERACOES TABELA PEDIDO
    # =========================================================

    op.create_index(
        op.f("ix_comanda_imprime"),
        "comanda",
        ["imprime"],
        unique=False,
    )

    op.add_column(
        "pedido",
        sa.Column(
            "tipo",
            tipo_pedido_enum,
            nullable=False,
            server_default="LOCAL",
        ),
    )

    op.add_column(
        "pedido",
        sa.Column(
            "endereco_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.alter_column(
        "pedido",
        "numero_mesa",
        existing_type=sa.INTEGER(),
        nullable=True,
    )

    op.alter_column(
        "pedido",
        "comanda_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )

    op.create_index(
        op.f("ix_pedido_endereco_id"),
        "pedido",
        ["endereco_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_pedido_tipo"),
        "pedido",
        ["tipo"],
        unique=False,
    )

    op.create_foreign_key(
        None,
        "pedido",
        "endereco",
        ["endereco_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    # =========================================================
    # PEDIDO
    # =========================================================

    op.drop_constraint(
        None,
        "pedido",
        type_="foreignkey",
    )

    op.drop_index(
        op.f("ix_pedido_tipo"),
        table_name="pedido",
    )

    op.drop_index(
        op.f("ix_pedido_endereco_id"),
        table_name="pedido",
    )

    op.alter_column(
        "pedido",
        "comanda_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )

    op.alter_column(
        "pedido",
        "numero_mesa",
        existing_type=sa.INTEGER(),
        nullable=False,
    )

    op.drop_column("pedido", "endereco_id")
    op.drop_column("pedido", "tipo")

    # =========================================================
    # COMANDA
    # =========================================================

    op.drop_index(
        op.f("ix_comanda_imprime"),
        table_name="comanda",
    )

    # =========================================================
    # ENDERECO
    # =========================================================

    op.drop_index(
        op.f("ix_endereco_atual"),
        table_name="endereco",
    )

    op.drop_index(
        op.f("ix_endereco_cliente_id"),
        table_name="endereco",
    )

    op.drop_table("endereco")

    # =========================================================
    # CLIENTE
    # =========================================================

    op.drop_index(
        op.f("ix_cliente_telefone"),
        table_name="cliente",
    )

    op.drop_table("cliente")

    # =========================================================
    # ENUM
    # =========================================================

    tipo_pedido_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )
