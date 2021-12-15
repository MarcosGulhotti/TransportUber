from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity
import sqlalchemy
from app.controllers.Utils.verificar_usuario import verificar_motorista
from app.exceptions.exc import NaoMotoristaError, PlacaFormatError
from app.models.caminhao_model import CaminhaoModel
from werkzeug.exceptions import NotFound

@jwt_required()
def criar_caminhao():
  session = current_app.db.session
  data = request.get_json()
  current_user = get_jwt_identity()

  data['marca'] = data['marca'].title()
  data['modelo'] = data['modelo'].title()
  data['placa'] = data['placa'].upper()
  try:
    verificar_motorista(current_user)
    data['motorista_id'] = current_user['id']
    novo_caminhao = CaminhaoModel(**data)
    session.add(novo_caminhao)
    session.commit()

  except sqlalchemy.exc.IntegrityError:
    return {"error": "Caminhão com esta placa já foi registrado"}, 400
  except PlacaFormatError as e:
    return {'msg': str(e)}, 400
  except NaoMotoristaError:
    return {"error": "Você não esta logado como um motorista"}, 401
  return jsonify(novo_caminhao.serialize()), 201

@jwt_required()
def listar_caminhoes():
  caminhoes = (CaminhaoModel.query.all())

  lista_caminhoes = [caminhao.serialize() for caminhao in caminhoes]

  return jsonify(lista_caminhoes), 200

@jwt_required()
def atualizar_caminhao(caminhao_id: int):
  try:
    session = current_app.db.session
    caminhao = CaminhaoModel.query.get(caminhao_id)
    data = request.get_json()
    current_user = get_jwt_identity()
    
    verificar_motorista(current_user)
    colunas_validas = ["capacidade_de_carga", "placa"]

    for k, v in data.items():
      if k in colunas_validas:
        setattr(caminhao, k, v)
      else:
        return {"error": f"Chave inválida: ({k})"}, 409

    session.add(caminhao)
    session.commit()

    return caminhao.serialize()

  except KeyError as e:
    return {"error": f"Chaves faltantes: {e.args}"}
  except PlacaFormatError as e:
    return {'msg': str(e)}, 400
  except NaoMotoristaError:
    return {"error": "Você não esta logado como um motorista"}, 401

@jwt_required()
def deletar_caminhao(caminhao_id):
  try:
    current_user = get_jwt_identity()
    verificar_motorista(current_user)

    caminhao_deletado = CaminhaoModel.query.filter_by(
      id=caminhao_id).first_or_404(description="Caminhão não encontrado")

    current_app.db.session.delete(caminhao_deletado)
    current_app.db.session.commit()

    return "", 204
    
  except NotFound:
    return jsonify({"erro": "Caminhão não existe."}), 404
  except NaoMotoristaError:
    return {"error": "Você não esta logado como um motorista"}, 401
      