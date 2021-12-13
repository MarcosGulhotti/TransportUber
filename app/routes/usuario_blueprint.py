from flask import Blueprint
from app.controllers.usuario_controller import deletar_usuario, atualizar_usuario, listar_usuario_id, listar_usuarios
from app.controllers.carga_controller import atualizar_carga, atualizar_disponivel, criar_carga, deletar_carga, listar_carga_id, listar_carga_origem, listar_carga_destino

bp_usuario = Blueprint('bp_usuario', __name__, url_prefix='/usuario')

# Rotas Usuarios
bp_usuario.get('')(listar_usuarios)
bp_usuario.get('/<int:usuario_id>')(listar_usuario_id)
bp_usuario.delete('')(deletar_usuario)
bp_usuario.patch('')(atualizar_usuario)


# Rotas Carga
bp_usuario.post('/carga')(criar_carga)
bp_usuario.get('/carga/<int:carga_id>')(listar_carga_id)

# virar uma rota só com query params
bp_usuario.get('/carga/origem/<origem>')(listar_carga_origem)
bp_usuario.get('/carga/destino/<destino>')(listar_carga_destino)

bp_usuario.patch('/carga/<int:carga_id>')(atualizar_carga)
bp_usuario.patch('/carga/<int:carga_id>/disponibilidade')(atualizar_disponivel)
bp_usuario.delete('/carga/<int:carga_id>')(deletar_carga)
