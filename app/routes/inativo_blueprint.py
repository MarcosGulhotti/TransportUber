from flask import Blueprint
from app.controllers.inativo_controller import desativar_usuario, reativar_usuario

bp_inativo = Blueprint('bp_inativo', __name__, url_prefix='/config')

bp_inativo.patch('/desativa')(desativar_usuario)
bp_inativo.patch('/ativa')(reativar_usuario)