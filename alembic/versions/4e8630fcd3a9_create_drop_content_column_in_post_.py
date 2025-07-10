"""create_drop content column in post_alembic table

Revision ID: 4e8630fcd3a9
Revises: f91d226a1833
Create Date: 2025-07-10 10:30:08.786311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e8630fcd3a9'
down_revision: Union[str, Sequence[str], None] = 'f91d226a1833'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts_alembic', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts_alembic', 'content')
    pass