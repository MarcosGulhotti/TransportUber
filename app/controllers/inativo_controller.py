from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.motorista_model import MotoristaModel
from app.models.usuario_model import UsuarioModel
from sqlalchemy.exc import IntegrityError

@jwt_required()
def desativar_usuario():
  session = current_app.db.session
  current_user = get_jwt_identity()

  if type(current_user) == dict:
    try:
      usuario: MotoristaModel = MotoristaModel.query.filter_by(id=current_user['id']).first()
      setattr(usuario, 'motorista_ativo', False)

      session.commit()
      return {'msg': "Motorista desativado com sucesso"}, 200
    except KeyError:
      return {"error": "Você não esta logado como Motorista"}, 401
    except IntegrityError:
      return {"error": "Usuário ou Motorista já foi desativado."}, 409
    except AttributeError:
      return {"error": "Usuário ou Motorista não existe."}, 409

  elif type(current_user) == int:
    try:
      usuario: UsuarioModel = UsuarioModel.query.filter_by(id=current_user).first()
      setattr(usuario, 'usuario_ativo', False)

      session.commit()
      return {'msg': "Usuario desativado com sucesso"}, 200
    except KeyError:
      return {"error": "Você não esta logado como Usuario"}, 401
    except IntegrityError:
      return {"error": "Usuário ou Motorista já foi desativado."}, 409
    except AttributeError:
      return {"error": "Usuário ou Motorista não existe."}, 409
            
@jwt_required()
def reativar_usuario():
  session = current_app.db.session
  current_user = get_jwt_identity()

  if type(current_user) == dict:
    try:
      usuario: MotoristaModel = MotoristaModel.query.filter_by(id=current_user['id']).first()
      setattr(usuario, 'motorista_ativo', True)

      session.commit()
      return {'msg': "Motorista re-ativado com sucesso"}, 200
    except KeyError:
      return {"error": "Você não esta logado como Motorista"}, 401
    except IntegrityError:
      return {"error": "Usuário ou Motorista já foi re-ativado."}, 409
    except AttributeError:
      return {"error": "Usuário ou Motorista não existe."}, 409

  elif type(current_user) == int:
    try:
      usuario: UsuarioModel = UsuarioModel.query.filter_by(id=current_user).first()
      setattr(usuario, 'usuario_ativo', True)

      session.commit()
      return {'msg': "Usuario re-ativado com sucesso"}, 200
    except KeyError:
      return {"error": "Você não esta logado como Usuario"}, 401
    except IntegrityError:
      return {"error": "Usuário ou Motorista já foi re-ativado."}, 409
    except AttributeError:
      return {"error": "Usuário ou Motorista não existe."}, 409
    

