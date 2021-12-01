"""empty message

Revision ID: 18a1a0d39e36
Revises: ccb4e5a353ff
Create Date: 2021-12-01 16:21:56.811623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18a1a0d39e36'
down_revision = 'ccb4e5a353ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('motoristas', sa.Column('password_hash', sa.String(length=255), nullable=False))
    op.add_column('usuarios', sa.Column('password_hash', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuarios', 'password_hash')
    op.drop_column('motoristas', 'password_hash')
    # ### end Alembic commands ###