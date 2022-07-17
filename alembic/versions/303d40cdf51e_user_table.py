"""user table

Revision ID: 303d40cdf51e
Revises: 5b8951042c60
Create Date: 2022-07-16 23:58:32.011839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '303d40cdf51e'
down_revision = '5b8951042c60'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
