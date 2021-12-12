"""empty message

Revision ID: 2e96a43fda60
Revises: acc2792f9489
Create Date: 2021-12-12 01:08:48.370527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e96a43fda60'
down_revision = 'acc2792f9489'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cargas', sa.Column('valor_frete', sa.Float(), nullable=False))
    op.add_column('cargas', sa.Column('valor_frete_motorista', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cargas', 'valor_frete_motorista')
    op.drop_column('cargas', 'valor_frete')
    # ### end Alembic commands ###
