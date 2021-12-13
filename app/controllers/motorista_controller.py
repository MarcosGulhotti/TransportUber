from flask import jsonify, request, current_app
from flask_jwt_extended.utils import get_jwt_identity
from app.exceptions.exc import CelularFormatError, CpfFormatError, LoginKeysError, RequiredKeysError
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

  try:
    chaves_necessarias = ['nome', 'sobrenome', 'password', 'cpf', 'cnh','email', 'celular']
    for key in chaves_necessarias:
      if key not in data:
        raise RequiredKeysError(f'Está faltando a chave ({key}).')
    
    chaves_model = ['nome', 'sobrenome', 'password', 'cpf', 'cnh','email', 'celular', 'motorista_ativo', 'created_at', 'updated_at']
    for key in data:
      if key not in chaves_model:
        raise RequiredKeysError(f'A chave ({key}) não é necessária.')

    novo_motorista = MotoristaModel(**data)

    password_to_hash = data.pop('password')
    novo_motorista.password = password_to_hash

    session.add(novo_motorista)
    session.commit()

    return jsonify(novo_motorista), 201
  except IntegrityError as e:
    assert isinstance(e.orig, UniqueViolation)
    return {'msg': 'CPF, CNH, email ou celular já cadastrado.'}, 409
  except CpfFormatError as e:
    return {'msg': str(e)}, 400
  except CelularFormatError as e:
    return {'msg': str(e)}, 400
  except RequiredKeysError as e:
    return {'msg': str(e)}, 400


def acesso_motorista():
  data = request.get_json()

  try:
    motorista: MotoristaModel = MotoristaModel.query.filter_by(email=data['email']).first()

    if not motorista:
      return {"msg": "Motorista não encontrado."}, 404

    chaves_necessarias = ['password','email']
    for key in chaves_necessarias:
      if key not in data:
        raise LoginKeysError(f'A chave ({key}) é necessária.')
    
    if motorista.verify_password(data['password']):
      access_token = create_access_token(identity=motorista.id)
      return jsonify(access_token=access_token), 200
    else:
      return {'msg': "Sem autorização"}, 401
  except KeyError:
    return {'msg': 'A chave (email) é necessária.'}
  except LoginKeysError as e:
    return {'msg': str(e)}, 400


@jwt_required()
def listar_motorista_por_id(id: int):
  try:
    motorista = MotoristaModel.query.get(id)

    return jsonify(motorista.serialize()), 200
  
  except AttributeError:
    return jsonify({"msg": "Motorista não existe."}), 404

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

  cidade = localizacao["address"]["village"]
  estado = localizacao["address"]["state"]

  dados = {
    "updated_at": datetime.now(),
    "localizacao": f"{cidade}/{estado}",
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
  
  return {"msg": "Senha atualizada"}, 200

