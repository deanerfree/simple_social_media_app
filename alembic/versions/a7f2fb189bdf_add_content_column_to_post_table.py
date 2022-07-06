"""add content column to post table


Revision ID: a7f2fb189bdf
Revises: f5d7da9090b7
Create Date: 2022-07-06 06:53:25.830504

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7f2fb189bdf'
down_revision = 'f5d7da9090b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
