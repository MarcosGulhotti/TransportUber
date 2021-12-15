from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

from app.exceptions.exc import NaoMotoristaError, NaoUsuarioError


@jwt_required()
def verificar_usuario(current_user):
    """Verificar se usuario atual é do tipo usuario"""
    current_user = get_jwt_identity()
    if type(current_user) == dict:
      raise NaoUsuarioError
    else: return True

jwt_required()
def verificar_motorista(current_user):
    """Verificar se motorista atual é do tipo usuario"""
    current_user = get_jwt_identity()
    if type(current_user) == int:
      raise NaoMotoristaError
    else: return True