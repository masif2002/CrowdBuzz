"""add content column

Revision ID: 043bdf6fcef1
Revises: 55842dba425c
Create Date: 2022-01-17 20:29:48.100227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '043bdf6fcef1'
down_revision = '55842dba425c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))

def downgrade():
    op.drop_column('posts', 'content')
