from flask import Blueprint
from app.controllers.inativo_controller import desativar_usuario

bp_inativo = Blueprint('bp_inativo', __name__, url_prefix='/desativacao')

bp_inativo.post('')(desativar_usuario)