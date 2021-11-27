from flask import Blueprint
from app.controllers.usuario_controller import criar_usuario

bp_usuario = Blueprint('bp_usuario', __name__, url_prefix='/usuario')

bp_usuario.post('')(criar_usuario)