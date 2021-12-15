from flask import Blueprint
from app.controllers.carga_controller import pegar_carga
from app.controllers.motorista_controller import atualizar_localizacao, atualizar_motorista, atualizar_senha, listar_motorista_por_id, listar_motoristas
from app.controllers.caminhao_controller import atualizar_caminhao, criar_caminhao, deletar_caminhao, listar_caminhoes

bp_motorista = Blueprint('bp_motorista', __name__, url_prefix='/motorista')

# Rotas Motorista
bp_motorista.get('')(listar_motoristas)
bp_motorista.get('/<int:id>')(listar_motorista_por_id)
bp_motorista.patch('/localizacao')(atualizar_localizacao)
bp_motorista.patch('/senha')(atualizar_senha)
bp_motorista.patch('')(atualizar_motorista)

# Rotas Caminhões
bp_motorista.post('/caminhao')(criar_caminhao)
bp_motorista.get('/caminhoes')(listar_caminhoes)
bp_motorista.patch('/caminhoes/<int:caminhao_id>')(atualizar_caminhao)
bp_motorista.delete('/caminhao/<int:caminhao_id>')(deletar_caminhao)

bp_motorista.patch('/carga/<int:carga_id>/pegar')(pegar_carga)