from flask import Blueprint
from app.controllers.categoria_controller import criar_categoria

bp_categoria = Blueprint('bp_categoria', __name__, url_prefix='/categoria')

bp_categoria.post('')(criar_categoria)
