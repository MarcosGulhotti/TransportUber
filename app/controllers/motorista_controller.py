from flask import jsonify, request, current_app
from flask_jwt_extended.utils import get_jwt_identity
from app.exceptions.exc import CpfFormatError
from app.models.motorista_model import MotoristaModel
from datetime import datetime
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import NotFound
from flask_jwt_extended import jwt_required
from geopy.geocoders import Nominatim
import time
import json


def criar_motorista():
  session = current_app.db.session
  data = request.get_json()

  data['nome'] = data['nome'].title()
  data['sobrenome'] = data['sobrenome'].title()
  data['created_at'] = datetime.now()

  password_to_hash = data.pop('password')

  try:
    novo_motorista = MotoristaModel(**data)
    novo_motorista.password = password_to_hash

    session.add(novo_motorista)
    session.commit()

    return jsonify(novo_motorista), 201
  except IntegrityError as e:
    assert isinstance(e.orig, UniqueViolation)
    return {'msg': 'CPF ou CNH já cadastrados.'}, 409
  except CpfFormatError as e:
    return {'msg': str(e)}, 400


def acesso_motorista():
  data = request.get_json()

  motorista: MotoristaModel = MotoristaModel.query.filter_by(email=data['email']).first()

  if not motorista:
    return {"msg": "Motorista nao encontrado."}, 404
  
  if motorista.verify_password(data['password']):
    access_token = create_access_token(identity=data['email'])
    return jsonify(access_token=access_token), 200
  else:
    return {'msg': "Sem autorização"}, 401

@jwt_required()
def listar_motorista_por_id(id: int):
  motorista = MotoristaModel.query.get(id)
  
  return jsonify(motorista.serialize()), 200

@jwt_required()
def listar_motoristas():
  motoristas = (MotoristaModel.query.all())

  lista_motoristas = [motorista.serialize() for motorista in motoristas]

  return jsonify(lista_motoristas), 200

@jwt_required()
def deletar_motorista():
  try:
    current_user = get_jwt_identity()
    motorista_deletado = MotoristaModel.query.filter_by(
      id=current_user).first_or_404(description="Usuário não encontrado")

    current_app.db.session.delete(motorista_deletado)
    current_app.db.session.commit()

    return "", 204
  except NotFound:
    return jsonify({"erro": "Usuário não existe"}), 404  
  
def busca_localizacao(latitude, longitude):
  geo = Nominatim(user_agent="transport_uber")
  coordenadas = f"{latitude}, {longitude}"
  time.sleep(3)
  try:
        return geo.reverse(coordenadas, language="pt-br").raw
  except:
      return busca_localizacao(latitude, longitude)

@jwt_required()
def atualizar_localizacao():
  session = current_app.db.session
  data = request.get_json()
  current_user = get_jwt_identity()

  motorista = MotoristaModel.query.filter(MotoristaModel.email == current_user).first()
  for k in data.keys():
      if k != "latitude" and k != "longitude":
          return {"error": "Chaves aceitas: [latitude, longitude]"}, 409
  
  latitude = float(data["latitude"])
  longitude = float(data["longitude"])
  localizacao = busca_localizacao(latitude=latitude, longitude=longitude)

  dados = {
    "updated_at": datetime.now(),
    "localizacao": json.dumps(localizacao["address"]),
    "latitude": latitude,
    "longitude": longitude
  }

  for k, v in dados.items():
    setattr(motorista, k, v)

  session.add(motorista)
  session.commit()

  return {"localizacao": motorista.localizacao}
  
@jwt_required()
def atualizar_senha():
  session = current_app.db.session
  data = request.get_json()
  current_user = get_jwt_identity()

  motorista = MotoristaModel.query.get(current_user)
  for k in data.keys():
      if k != "password":
          return {"error": "Chaves aceitas: [password]"}, 409

  data["updated_at"] = datetime.now()

  for k, v in data.items():
    setattr(motorista, k, v)

  session.add(motorista)
  session.commit()
  
  return {}, 204

