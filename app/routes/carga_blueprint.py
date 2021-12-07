from flask import Blueprint
from app.controllers.carga_controller import listar_carga

bp_carga = Blueprint('bp_carga', __name__, url_prefix='/carga')

bp_carga.get('/<int:carga_id>')(listar_carga)
