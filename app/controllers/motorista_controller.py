from flask import jsonify, request, current_app
from app.exceptions.exc import CpfFormatError
from app.models.motorista_model import MotoristaModel
from datetime import datetime
from app.models.caminhao_model import CaminhaoModel
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

def criar_motorista():
  session = current_app.db.session
  data = request.get_json()

  data['nome'] = data['nome'].title()
  data['sobrenome'] = data['sobrenome'].title()
  data['created_at'] = datetime.now()

  try:
    novo_motorista = MotoristaModel(**data)

    session.add(novo_motorista)
    session.commit()

    caminhoes = CaminhaoModel.query.filter_by(motorista_id=novo_motorista.id).all()

    return jsonify({
      'id': novo_motorista.id,
      'nome': novo_motorista.nome,
      'sobrenome': novo_motorista.sobrenome,
      'cpf': novo_motorista.cpf,
      'created_at': novo_motorista.created_at,
      'caminhoes': caminhoes
    }), 201
  except IntegrityError as e:
    assert isinstance(e.orig, UniqueViolation)
    return {'msg': 'CPF já cadastrado.'}, 409
  except CpfFormatError as e:
    return {'msg': str(e)}, 400

def listar_motorista_por_id(id: int):
  motorista = MotoristaModel.query.get(id)
  caminhoes = CaminhaoModel.query.filter_by(motorista_id=id).all()

  return jsonify({
    'nome': motorista.nome,
    'sobrenome': motorista.sobrenome,
    'caminhoes': caminhoes
  })