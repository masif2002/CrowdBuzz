"""add foreign-key

Revision ID: 7223fef98293
Revises: 88fb11965e20
Create Date: 2022-01-18 09:42:08.000363

"""
from alembic import op
from sqlalchemy import *


# revision identifiers, used by Alembic.
revision = '7223fef98293'
down_revision = '88fb11965e20'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', name="posts_users_fkey"), nullable=False))

def downgrade():
    #op.drop_constraint("posts_users_fkey", 'posts')
    op.drop_column('posts', 'user_id')
