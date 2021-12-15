from flask import Blueprint
from app.controllers.estado_controller import cria_estados
from app.controllers.municipio_controller import cria_municipios, deletar_municipios

bp_municipio = Blueprint('bp_municipio', __name__, url_prefix='/super_adm')

bp_municipio.post('/municipio')(cria_municipios)
bp_municipio.post('/estado')(cria_estados)

bp_municipio.delete('/municipio')(deletar_municipios)