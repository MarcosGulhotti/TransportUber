from flask import jsonify, request, current_app
from flask_jwt_extended.utils import get_jwt_identity
from app.exceptions.exc import CpfFormatError
from app.models.usuario_model import UsuarioModel
from datetime import datetime
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import NotFound
from flask_jwt_extended import jwt_required

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

def acesso_usuario():
  data = request.get_json()

  usuario: UsuarioModel = UsuarioModel.query.filter_by(email=data['email']).first()

  if not usuario:
    return {"msg": "Usuario nao encontrado."}, 404
  
  if usuario.verify_password(data['password']):
    access_token = create_access_token(identity=usuario.id)
    return jsonify(access_token=access_token), 200
  else:
    return {'msg': "Sem autorização"}, 401

@jwt_required()
def atualizar_usuario():
  data = request.json
  current_user = get_jwt_identity()

  try:
    UsuarioModel.query.filter_by(id=current_user).first_or_404()
    autorizado_mudar = ['password_hash', 'email', 'celular']

    for key in data:
      if key not in autorizado_mudar:
        return {"msg": f'Não é permitido modificar a chave {key}'}, 400

      data['updated_at'] = datetime.now()

      user = UsuarioModel.query.filter_by(id=current_user).update(data)
      current_app.db.session.commit()

      user = UsuarioModel.query.get(current_user)

      return jsonify(user), 200
    
  except NotFound:
    return jsonify({"msg": "Usuário não existe"}), 404  

@jwt_required()
def deletar_usuario():
  try:
    current_user = get_jwt_identity()
    usuario_deletado = UsuarioModel.query.filter_by(
      id=current_user).first_or_404(description="Usuário não encontrado")

    current_app.db.session.delete(usuario_deletado)
    current_app.db.session.commit()

    return "", 204
  except NotFound:
    return jsonify({"erro": "Usuário não existe"}), 404  
      
@jwt_required()
def listar_usuarios():
  usuarios = (UsuarioModel.query.all())

  lista_usuarios = [usuarios.serialize() for usuarios in usuarios]

  return jsonify(lista_usuarios), 200

@jwt_required()
def listar_usuario_id(usuario_id: int):
  usuario = UsuarioModel.query.filter_by(id=usuario_id).first()

  return jsonify(usuario.serialize()), 200