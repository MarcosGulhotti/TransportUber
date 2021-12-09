from flask import Blueprint
from app.controllers.carga_controller import atualizar_disponivel, listar_carga, atualizar_carga

bp_carga = Blueprint('bp_carga', __name__, url_prefix='/carga')

bp_carga.get('/<int:carga_id>')(listar_carga)
bp_carga.patch('/<int:carga_id>')(atualizar_carga)
bp_carga.patch('/<int:carga_id>/disponibilidade')(atualizar_disponivel)
