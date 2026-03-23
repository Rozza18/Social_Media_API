"""add last few tables to posts table

Revision ID: 77c3310bc56d
Revises: d4c37fae76f9
Create Date: 2026-03-22 23:29:46.499992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77c3310bc56d'
down_revision: Union[str, Sequence[str], None] = 'd4c37fae76f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column(
            'published',
            sa.Boolean(),
            nullable=False,
            server_default='True'
        )
    )
    op.add_column(
        'posts',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text('NOW()')
        ))
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        'posts',
        'published'
    )
    op.drop_column(
        'posts',
        'created_at'
    )
    pass
