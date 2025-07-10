"""create_drop foreign key to  posts_alembic table

Revision ID: e1d514ce3bea
Revises: 706144ce6a03
Create Date: 2025-07-10 10:42:30.076339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1d514ce3bea'
down_revision: Union[str, Sequence[str], None] = '706144ce6a03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts_alembic', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts_alembic", referent_table="users_alembic", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts_alembic")
    op.drop_column('posts_alembic', 'owner_id')
    pass