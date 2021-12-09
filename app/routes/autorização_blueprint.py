from flask import Blueprint
from app.controllers.usuario_controller import acesso_usuario, criar_usuario
from app.controllers.motorista_controller import criar_motorista, acesso_motorista

bp_autenticação = Blueprint('bp_autenticação', __name__, url_prefix='/autenticaçao')

bp_autenticação.post('/usuario/acesso')(acesso_usuario)
bp_autenticação.post('/usuario/registro')(criar_usuario)

bp_autenticação.post('/motorista/acesso')(acesso_motorista)
bp_autenticação.post('/motorista/registro')(criar_motorista)