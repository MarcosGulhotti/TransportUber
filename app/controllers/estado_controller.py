from flask.json import jsonify
from app.controllers.Utils.verificar_usuario import verificar_usuario
from app.services.estados import estados
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.exceptions.exc import NaoUsuarioError
from app.models.usuario_model import UsuarioModel
from flask import current_app
from app.models.estados_model import EstadoModel

@jwt_required()
def cria_estados():
  current_user = get_jwt_identity()
  session = current_app.db.session
  comprimento_tabela = len(EstadoModel.query.all())

  try:
    verificar_usuario(current_user)
    usuario: UsuarioModel = UsuarioModel.query.get(current_user)

    if usuario.super_adm:
      if comprimento_tabela == 0:
        for estado in estados:
          data = {
            "nome": estado['nome'].lower(),
            "codigo_uf": estado['codigo_uf'],
            "uf": estado['uf']
          }
          novo_estado = EstadoModel(**data)
          session.add(novo_estado)
          session.commit()
        return '', 200
      else:
        return {'error': "Tabela ja populada."}, 401
    
  except NaoUsuarioError:
    return {'error': "Você não tem permissão para acessar esta rota."}, 401
  except AttributeError:
    return {'error': "Você não tem permissão para acessar esta rota."}, 401


@jwt_required()
def listar_estados():
  estados: EstadoModel = EstadoModel.query.all()

  serialize = [estado.serialize() for estado in estados]

  return jsonify(serialize), 200


@jwt_required()
def listar_estados_por_codigo_uf(estado_uf: int):
  estados = EstadoModel.query.filter_by(codigo_uf=estado_uf).all()

  serialize = [estado.serialize() for estado in estados]

  return jsonify(serialize), 200