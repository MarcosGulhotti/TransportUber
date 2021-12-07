from flask import Blueprint
from app.controllers.usuario_controller import criar_usuario, login
from app.controllers.carga_controller import criar_carga, listar_carga_id, listar_carga_origem, listar_carga_destino

bp_usuario = Blueprint('bp_usuario', __name__, url_prefix='/usuario')

bp_usuario.post('')(criar_usuario)
bp_usuario.post('/<int:dono_id>/carga')(criar_carga)
bp_usuario.post('/login')(login)
bp_usuario.get('/carga/<int:carga_id>')(listar_carga_id)
bp_usuario.get('/carga/origem/<origem>')(listar_carga_origem)
bp_usuario.get('/carga/destino/<destino>')(listar_carga_destino)