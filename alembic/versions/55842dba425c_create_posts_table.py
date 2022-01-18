"""create posts table

Revision ID: 55842dba425c
Revises: 
Create Date: 2022-01-17 19:46:02.950820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55842dba425c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer, primary_key=True, nullable=False),
    sa.Column('title', sa.String, nullable=False))


def downgrade():
    op.drop_table('posts')
