from flask import Blueprint
from app.controllers.categoria_controller import criar_categoria, deletar_categoria

bp_categoria = Blueprint('bp_categoria', __name__, url_prefix='/categoria')

bp_categoria.post('')(criar_categoria)
bp_categoria.delete('/<int:categoria_id>')(deletar_categoria)