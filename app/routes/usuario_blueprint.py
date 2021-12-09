from flask import Blueprint
from app.controllers.usuario_controller import deletar_usuario, atualizar_usuario, listar_usuario_id, listar_usuarios
from app.controllers.carga_controller import criar_carga, listar_carga_id, listar_carga_origem, listar_carga_destino

bp_usuario = Blueprint('bp_usuario', __name__, url_prefix='/usuario')

bp_usuario.post('/<int:dono_id>/carga')(criar_carga)
bp_usuario.patch('/<int:usuario_id>')(atualizar_usuario)
bp_usuario.get('/carga/<int:carga_id>')(listar_carga_id)
bp_usuario.get('/carga/origem/<origem>')(listar_carga_origem)
bp_usuario.get('/carga/destino/<destino>')(listar_carga_destino)
bp_usuario.delete('/<int:usuario_id>')(deletar_usuario)
bp_usuario.get('')(listar_usuarios)
bp_usuario.get('/<int:usuario_id>')(listar_usuario_id)