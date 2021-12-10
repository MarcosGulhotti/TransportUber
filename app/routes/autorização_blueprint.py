from flask import Blueprint
from app.controllers.usuario_controller import acesso_usuario, criar_usuario
from app.controllers.motorista_controller import criar_motorista, acesso_motorista

bp_autenticacao = Blueprint('bp_autenticacao', __name__, url_prefix='/autenticacao')

bp_autenticacao.post('/usuario/acesso')(acesso_usuario)
bp_autenticacao.post('/usuario/registro')(criar_usuario)

bp_autenticacao.post('/motorista/acesso')(acesso_motorista)
bp_autenticacao.post('/motorista/registro')(criar_motorista)