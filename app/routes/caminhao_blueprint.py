from flask import Blueprint
from app.controllers.caminhao_controller import criar_caminhao

bp_caminhao = Blueprint('bp_caminhao', __name__, url_prefix='/caminhao')

bp_caminhao.post('')(criar_caminhao)