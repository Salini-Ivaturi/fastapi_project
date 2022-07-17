"""adding more columns to posts table

Revision ID: b19498ee4896
Revises: c26595de3b20
Create Date: 2022-07-17 00:23:21.801882

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b19498ee4896'
down_revision = 'c26595de3b20'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                     server_default=sa.text('NOW()'), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
