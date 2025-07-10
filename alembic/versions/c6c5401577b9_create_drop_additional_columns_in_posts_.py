"""create_drop additional columns in posts_alembic table

Revision ID: c6c5401577b9
Revises: e1d514ce3bea
Create Date: 2025-07-10 10:49:28.305788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6c5401577b9'
down_revision: Union[str, Sequence[str], None] = 'e1d514ce3bea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts_alembic', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts_alembic', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts_alembic', 'published')
    op.drop_column('posts_alembic', 'created_at')
    pass