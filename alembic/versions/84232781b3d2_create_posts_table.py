"""create posts table

Revision ID: 84232781b3d2
Revises: 
Create Date: 2022-07-16 21:29:11.143672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84232781b3d2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
