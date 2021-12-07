from flask import Blueprint
from app.controllers.usuario_controller import criar_usuario, login, update
from app.controllers.carga_controller import criar_carga

bp_usuario = Blueprint('bp_usuario', __name__, url_prefix='/usuario')

bp_usuario.post('')(criar_usuario)
bp_usuario.post('/<int:dono_id>/carga')(criar_carga)
bp_usuario.post('/login')(login)
bp_usuario.patch('/<int:user_id>')(update)