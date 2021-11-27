from flask import jsonify, request, current_app
from app.exceptions.exc import CpfFormatError
from app.models.usuario_model import UsuarioModel
from datetime import datetime
from app.models.carga_model import CargaModel
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

def criar_usuario():
  session = current_app.db.session
  data = request.get_json()

  data['nome'] = data['nome'].title()
  data['sobrenome'] = data['sobrenome'].title()
  data['created_at'] = datetime.now()

  try:
    novo_usuario = UsuarioModel(**data)

    session.add(novo_usuario)
    session.commit()

    cargas = CargaModel.query.filter_by(dono_id=novo_usuario.id).all()

    return jsonify({
      'nome': novo_usuario.nome,
      'sobrenome': novo_usuario.sobrenome,
      'cpf': novo_usuario.cpf,
      'created_at': novo_usuario.created_at,
      'cargas': cargas
    }), 201
  except IntegrityError as e:
    assert isinstance(e.orig, UniqueViolation)
    return {'msg': 'CPF já cadastrado.'}, 409
  except CpfFormatError as e:
    return {'msg': str(e)}, 400