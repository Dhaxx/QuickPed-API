"""Add min_selecoes to grupo_adicional

Revision ID: add_min_selecoes_grupo
Revises:
Create Date: 2025-04-20

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add_min_selecoes_grupo"
down_revision = "098bb0b53b75"  # último revision
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "grupo_adicional",
        sa.Column("min_selecoes", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("grupo_adicional", "min_selecoes")
