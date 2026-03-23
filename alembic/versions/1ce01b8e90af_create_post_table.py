"""create post table

Revision ID: 1ce01b8e90af
Revises: 
Create Date: 2026-03-22 21:28:41.997883

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ce01b8e90af'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None: #it runs this commands to do the change that we want
    """Upgrade schema."""
    # create table with two columns id and title first
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None: #it handle removing the changes
    """Downgrade schema."""
    op.drop_table('posts')
    pass
