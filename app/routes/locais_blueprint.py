from flask import Blueprint
from app.controllers.estado_controller import listar_estados, listar_estados_por_codigo_uf
from app.controllers.municipio_controller import listar_municipios,listar_municipios_por_estado

bp_local = Blueprint('bp_local', __name__, url_prefix='/localizacao')

bp_local.get('/municipios')(listar_municipios)
bp_local.get('/municipio/estado/<int:estado_uf>')(listar_municipios_por_estado)
bp_local.get('/estados')(listar_estados)
bp_local.get('/estado/<int:estado_uf>')(listar_estados_por_codigo_uf)