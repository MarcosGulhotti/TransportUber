"""empty message

Revision ID: 199bb6d42220
Revises: f7f226b2b14e
Create Date: 2021-11-30 16:03:49.656401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '199bb6d42220'
down_revision = 'f7f226b2b14e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cargas', 'caminhao_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('cargas_caminhao_id_key', 'cargas', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('cargas_caminhao_id_key', 'cargas', ['caminhao_id'])
    op.alter_column('cargas', 'caminhao_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
