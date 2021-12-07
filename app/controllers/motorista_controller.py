from flask import jsonify, request, current_app
from app.exceptions.exc import CpfFormatError
from app.models.motorista_model import MotoristaModel
from datetime import datetime
from app.models.caminhao_model import CaminhaoModel
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

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

def login():
  data = request.get_json()

  motorista: MotoristaModel = MotoristaModel.query.filter_by(cpf=data['cpf']).first()

  if not motorista:
    return {"msg": "Motorista nao encontrado."}, 404
  
  if motorista.verify_password(data['password']):
    access_token = create_access_token(identity=data['cpf'])
    return jsonify(access_token=access_token), 200
  else:
    return {'msg': "Sem autorização"}, 401

def listar_motorista_por_id(id: int):
  motorista = MotoristaModel.query.get(id)
  
  return jsonify(motorista.serialize()), 201


def listar_motoristas():
  motoristas = (MotoristaModel.query.all())

  lista_motoristas = [motorista.serialize() for motorista in motoristas]

  return jsonify(lista_motoristas), 201
