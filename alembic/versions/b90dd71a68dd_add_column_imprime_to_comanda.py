"""add column imprime to comanda

Revision ID: b90dd71a68dd
Revises: 9162a9a0283a
Create Date: 2026-04-24 16:54:56.969456

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b90dd71a68dd"
down_revision: Union[str, Sequence[str], None] = "9162a9a0283a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "comanda",
        sa.Column("imprime", sa.Boolean(), nullable=False, server_default="false"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("comanda", "imprime")
