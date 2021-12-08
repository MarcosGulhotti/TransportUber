from flask import Blueprint
from app.controllers.motorista_controller import criar_motorista, deletar_motorista, listar_motorista_por_id, listar_motoristas, login
from app.controllers.caminhao_controller import criar_caminhao, deletar_caminhao, listar_caminhoes

bp_motorista = Blueprint('bp_motorista', __name__, url_prefix='/motorista')

bp_motorista.post('')(criar_motorista)
bp_motorista.get('')(listar_motoristas)
bp_motorista.get('/<int:id>')(listar_motorista_por_id)
bp_motorista.delete('/<int:id_motorista>')(deletar_motorista)
bp_motorista.post('/<int:motorista_id>/caminhao')(criar_caminhao)
bp_motorista.get('/caminhoes')(listar_caminhoes)
bp_motorista.delete('/caminhao/<int:caminhao_id>')(deletar_caminhao)
bp_motorista.post('/login')(login)