"""add content column to posts table

Revision ID: d3d5371066aa
Revises: 1ce01b8e90af
Create Date: 2026-03-22 23:05:57.449347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3d5371066aa'
down_revision: Union[str, Sequence[str], None] = '1ce01b8e90af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
