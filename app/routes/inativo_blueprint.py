from flask import Blueprint
from app.controllers.inativo_controller import desativar_usuario, reativar_usuario

bp_inativo = Blueprint('bp_inativo', __name__, url_prefix='/desativacao')

bp_inativo.post('')(desativar_usuario)
bp_inativo.patch('/reativacao')(reativar_usuario)