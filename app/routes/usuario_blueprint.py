from flask import Blueprint
from app.controllers.avaliacao_controller import avaliar_usuario
from app.controllers.usuario_controller import atualizar_senha, atualizar_usuario, listar_usuario_id, listar_usuarios
from app.controllers.carga_controller import atualizar_carga, criar_carga, deletar_carga, listar_carga_id, listar_carga_origem, listar_carga_destino, confirmar_entrega, listar_cargas, listar_cargas_entregues

bp_usuario = Blueprint('bp_usuario', __name__, url_prefix='/usuario')

# Rotas Usuarios
bp_usuario.get('')(listar_usuarios)
bp_usuario.get('/<int:usuario_id>')(listar_usuario_id)
bp_usuario.patch('')(atualizar_usuario)
bp_usuario.patch('/senha')(atualizar_senha)

# Rotas Carga
bp_usuario.post('/carga')(criar_carga)
bp_usuario.get('/carga/<int:carga_id>')(listar_carga_id)
bp_usuario.get('/carga/cargas_entregues')(listar_cargas_entregues)
bp_usuario.post('/carga/<int:carga_id>/entrega_concluida')(confirmar_entrega)

# virar uma rota só com query params
bp_usuario.get('/carga/origem/<origem>')(listar_carga_origem)
bp_usuario.get('/carga/destino/<destino>')(listar_carga_destino)

bp_usuario.patch('/carga/<int:carga_id>')(atualizar_carga)
bp_usuario.delete('/carga/<int:carga_id>')(deletar_carga)

# rota com query
bp_usuario.get("/carga")(listar_cargas)

bp_usuario.post('/avaliacoes')(avaliar_usuario)
