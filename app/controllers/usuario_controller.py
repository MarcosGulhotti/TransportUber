from os import access
from flask import jsonify, request, current_app
from app.exceptions.exc import CpfFormatError
from app.models.usuario_model import UsuarioModel
from datetime import datetime
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import NotFound

def criar_usuario():
  session = current_app.db.session
  data = request.get_json()

  data['nome'] = data['nome'].title()
  data['sobrenome'] = data['sobrenome'].title()
  data['created_at'] = datetime.now()

  password_to_hash = data.pop('password')

  try:
    novo_usuario = UsuarioModel(**data)
    novo_usuario.password = password_to_hash

    session.add(novo_usuario)
    session.commit()

    return jsonify(novo_usuario), 201
  except IntegrityError as e:
    assert isinstance(e.orig, UniqueViolation)
    return {'msg': 'CPF já cadastrado.'}, 409
  except CpfFormatError as e:
    return {'msg': str(e)}, 400

def login():
  data = request.get_json()

  usuario: UsuarioModel = UsuarioModel.query.filter_by(cpf=data['cpf']).first()

  if not usuario:
    return {"msg": "Usuario nao encontrado."}, 404
  
  if usuario.verify_password(data['password']):
    access_token = create_access_token(identity=data['cpf'])
    return jsonify(access_token=access_token), 200
  else:
    return {'msg': "Sem autorização"}, 401


def atualizar_usuario(usuario_id: int):
  data = request.json

  try:
    UsuarioModel.query.filter_by(id=usuario_id).first_or_404()
    autorizado_mudar = ['password_hash', 'email', 'celular']

    for key in data:
      if key not in autorizado_mudar:
        print(data)
        return {"msg": f'Não é permitido modificar a chave {key}'}, 400

      data['updated_at'] = datetime.now()

      user = UsuarioModel.query.filter_by(id=usuario_id).update(data)
      current_app.db.session.commit()

      user = UsuarioModel.query.get(usuario_id)

      return jsonify(user), 200
    
  except NotFound:
    return jsonify({"msg": "Usuário não existe"}), 404  


def deletar_usuario(usuario_id):
  try:
    usuario_deletado = UsuarioModel.query.filter_by(
      id=usuario_id).first_or_404(description="Usuário não encontrado")

    current_app.db.session.delete(usuario_deletado)
    current_app.db.session.commit()

    return "", 204
  except NotFound:
    return jsonify({"erro": "Usuário não existe"}), 404  
      
  