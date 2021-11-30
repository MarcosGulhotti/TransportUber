from flask import Blueprint
from app.controllers.motorista_controller import criar_motorista, listar_motorista_por_id
from app.controllers.caminhao_controller import criar_caminhao

bp_motorista = Blueprint('bp_motorista', __name__, url_prefix='/motorista')

bp_motorista.post('')(criar_motorista)
bp_motorista.get('/<int:id>')(listar_motorista_por_id)
bp_motorista.post('/<int:motorista_id>/caminhao')(criar_caminhao)