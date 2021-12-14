from flask import Blueprint
from app.controllers.municipio_controller import cria_municipios

bp_municipio = Blueprint('bp_municipio', __name__, url_prefix='/super_adm')

bp_municipio.post('/municipio')(cria_municipios)
