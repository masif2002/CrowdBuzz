"""add rest of the columns

Revision ID: 84160f4fa2aa
Revises: 7223fef98293
Create Date: 2022-01-18 09:59:29.266013

"""
from alembic import op
from sqlalchemy import *


# revision identifiers, used by Alembic.
revision = '84160f4fa2aa'
down_revision = '7223fef98293'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', Column('published', Boolean, server_default='TRUE', nullable=False))
    op.add_column('posts', Column('created_at', TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
