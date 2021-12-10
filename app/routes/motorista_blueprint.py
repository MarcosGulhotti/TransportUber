from flask import Blueprint
from app.controllers.motorista_controller import atualizar_localizacao, atualizar_senha, deletar_motorista, listar_motorista_por_id, listar_motoristas
from app.controllers.caminhao_controller import atualizar_caminhao, criar_caminhao, deletar_caminhao, listar_caminhoes

bp_motorista = Blueprint('bp_motorista', __name__, url_prefix='/motorista')

bp_motorista.get('')(listar_motoristas)
bp_motorista.get('/<int:id>')(listar_motorista_por_id)
bp_motorista.delete('/<int:motorista_id>')(deletar_motorista)
bp_motorista.delete('/caminhao/<int:caminhao_id>')(deletar_caminhao)
bp_motorista.post('/<int:motorista_id>/caminhao')(criar_caminhao)
bp_motorista.get('/caminhoes')(listar_caminhoes)
bp_motorista.patch('/caminhoes/<int:caminhao_id>')(atualizar_caminhao)
bp_motorista.patch('/<int:id>/localizacao')(atualizar_localizacao)
bp_motorista.patch('/<int:id>/senha')(atualizar_senha)
