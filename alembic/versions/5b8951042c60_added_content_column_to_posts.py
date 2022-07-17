"""added content column to posts

Revision ID: 5b8951042c60
Revises: 84232781b3d2
Create Date: 2022-07-16 21:39:26.305132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b8951042c60'
down_revision = '84232781b3d2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
