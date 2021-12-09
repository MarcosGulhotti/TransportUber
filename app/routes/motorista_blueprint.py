from flask import Blueprint
from app.controllers.motorista_controller import atualizar_localizacao, atualizar_senha, criar_motorista, listar_motorista_por_id, listar_motoristas, login
from app.controllers.caminhao_controller import criar_caminhao, listar_caminhoes

bp_motorista = Blueprint('bp_motorista', __name__, url_prefix='/motorista')

bp_motorista.post('')(criar_motorista)
bp_motorista.get('')(listar_motoristas)
bp_motorista.get('/<int:id>')(listar_motorista_por_id)
bp_motorista.post('/<int:motorista_id>/caminhao')(criar_caminhao)
bp_motorista.get('/caminhoes')(listar_caminhoes)
bp_motorista.post('/login')(login)
bp_motorista.patch('/caminhoes/<int:caminhao_id>')
bp_motorista.patch('/<int:id>/localizacao')(atualizar_localizacao)
bp_motorista.patch('/<int:id>/senha')(atualizar_senha)