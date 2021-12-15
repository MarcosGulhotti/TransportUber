from flask.json import jsonify
from app.controllers.Utils.verificar_usuario import verificar_usuario
from app.services.municipios import municipios
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.exceptions.exc import NaoUsuarioError
from app.models.usuario_model import UsuarioModel
from flask import current_app
from app.models.municipios_model import MunicipioModel

@jwt_required()
def cria_municipios():
  current_user = get_jwt_identity()
  session = current_app.db.session
  comprimento_tabela = len(MunicipioModel.query.all())

  try:
    verificar_usuario(current_user)
    usuario: UsuarioModel = UsuarioModel.query.get(current_user)

    if usuario.super_adm:
      if comprimento_tabela == 0:
        for municipio in municipios:
          data = {
            "codigo_uf": municipio['codigo_uf'],
            "nome": municipio['nome'].lower(),
            "latitude": municipio['latitude'],
            "longitude": municipio['longitude']
          }
          novo_municipio = MunicipioModel(**data)
          session.add(novo_municipio)
          session.commit()
        return '', 200
      else:
        return {'error': "Tabela ja populada."}, 401
    
  except NaoUsuarioError:
    return {'error': "Você não tem permissão para acessar esta rota."}, 401
  except AttributeError:
    return {'error': "Você não tem permissão para acessar esta rota."}, 401


@jwt_required()
def listar_municipios():
  municipios: MunicipioModel = MunicipioModel.query.all()

  serialize = [municipio.serialize() for municipio in municipios]

  return jsonify(serialize), 200