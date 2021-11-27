"""criação das tabelas: usuarios, motoristas, cargas e caminhoes

Revision ID: 8d10112e501e
Revises: 
Create Date: 2021-11-27 16:15:44.758548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d10112e501e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('motoristas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('sobrenome', sa.String(), nullable=False),
    sa.Column('cpf', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('sobrenome', sa.String(), nullable=False),
    sa.Column('cpf', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf')
    )
    op.create_table('caminhoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('marca', sa.String(), nullable=False),
    sa.Column('modelo', sa.String(), nullable=False),
    sa.Column('capacidade_de_carga', sa.Float(), nullable=False),
    sa.Column('motorista_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['motorista_id'], ['motoristas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cargas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('disponivel', sa.Boolean(), nullable=False),
    sa.Column('destino', sa.String(), nullable=False),
    sa.Column('origem', sa.String(), nullable=False),
    sa.Column('horario_saida', sa.DateTime(), nullable=True),
    sa.Column('horario_chegada', sa.DateTime(), nullable=True),
    sa.Column('peso', sa.Float(), nullable=False),
    sa.Column('caminhao_id', sa.Integer(), nullable=False),
    sa.Column('dono_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['caminhao_id'], ['caminhoes.id'], ),
    sa.ForeignKeyConstraint(['dono_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('caminhao_id'),
    sa.UniqueConstraint('dono_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cargas')
    op.drop_table('caminhoes')
    op.drop_table('usuarios')
    op.drop_table('motoristas')
    # ### end Alembic commands ###
