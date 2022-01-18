"""add users table

Revision ID: 88fb11965e20
Revises: 043bdf6fcef1
Create Date: 2022-01-17 20:37:16.951993

"""
from alembic import op
from sqlalchemy import *


# revision identifiers, used by Alembic.
revision = '88fb11965e20'
down_revision = '043bdf6fcef1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
    Column('id', Integer, nullable=False),
    Column('email', String, nullable=False),
    Column('password', String, nullable=False),
    Column('created_at', TIMESTAMP(timezone=True),nullable=False, server_default=text('now()')),
    PrimaryKeyConstraint('id'),
    UniqueConstraint('email')
    )


def downgrade():
   op.drop_table('users')
