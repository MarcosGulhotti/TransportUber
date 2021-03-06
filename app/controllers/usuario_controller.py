from flask import jsonify, request, current_app
from flask_jwt_extended.utils import get_jwt_identity
from app.controllers.Utils.calculo_frete_controller import calcular_frete, calcular_previsão_de_entrega, gerar_latitude_longitude
from app.controllers.Utils.verificar_usuario import verificar_usuario
from app.exceptions.exc import CelularFormatError, CpfFormatError, LoginKeysError, NaoUsuarioError, RequiredKeysError
from app.models.avaliacao_usuario_motorista_model import AvaliacaoUsuarioMotoristaModel
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

  try:
    chaves_necessarias = ['nome', 'sobrenome', 'password', 'cpf', 'email', 'celular']
    for key in chaves_necessarias:
      if key not in data:
        raise RequiredKeysError(f'Está faltando a chave ({key}).')
    
    chaves_model = ['nome', 'sobrenome', 'password', 'cpf', 'email', 'celular', 'usuario_ativo', 'created_at', 'updated_at']
    for key in data:
      if key not in chaves_model and key != 'super_adm':
        raise RequiredKeysError(f'A chave ({key}) não é necessária.')
    
    password_to_hash = data.pop('password')

    novo_usuario = UsuarioModel(**data)
    novo_usuario.password = password_to_hash
    session.add(novo_usuario)

    usuario_id = UsuarioModel.query.filter_by(email=novo_usuario.email).first().id

    data = {
      "nota": 0, 
      "usuario_id": usuario_id
    }
    nova_avaliacao = AvaliacaoUsuarioMotoristaModel(**data)
    session.add(nova_avaliacao)

    session.commit()

    return jsonify(novo_usuario), 201
  except IntegrityError as e:
    assert isinstance(e.orig, UniqueViolation)
    return {'msg': 'CPF, email ou celular já cadastrado.'}, 409
  except CpfFormatError as e:
    return {'msg': str(e)}, 400
  except CelularFormatError as e:
    return {'msg': str(e)}, 400
  except RequiredKeysError as e:
    return {'msg': str(e)}, 400


def acesso_usuario():
  data = request.get_json()

  try:
    usuario: UsuarioModel = UsuarioModel.query.filter_by(email=data['email']).first()
    
    if not usuario:
      return {"msg": "Usuario nao encontrado."}, 404
    
    chaves_necessarias = ['password','email']
    for key in chaves_necessarias:
      if key not in data:
        raise LoginKeysError(f'A chave ({key}) é necessária.')
    
    if usuario.verify_password(data['password']):
      access_token = create_access_token(identity=usuario.id)
      return jsonify(access_token=access_token), 200
    else:
      return {'msg': "Sem autorização"}, 401
  
  except KeyError:
    return {'msg': 'A chave (email) é necessária.'}
  except LoginKeysError as e:
    return {'msg': str(e)}, 400


@jwt_required()
def atualizar_usuario():
  session = current_app.db.session
  data = request.json
  current_user = get_jwt_identity()

  try:
    verificar_usuario(current_user)
    usuario = UsuarioModel.query.get(current_user)
    autorizado_mudar = ['password', 'email', 'celular']

    for key in data:
      if key not in autorizado_mudar:
        return {"msg": f'Não é permitido modificar a chave ({key}).'}, 400

    data['updated_at'] = datetime.now()
    
    for key, value in data.items():
      setattr(usuario, key, value)

    session.add(usuario)
    session.commit()

    user = UsuarioModel.query.get(current_user)

    return jsonify(user.serialize()), 200
    
  except NotFound:
    return jsonify({"msg": "Usuário não existe"}), 404
  except NaoUsuarioError:
    return {"error": "Você não esta logado como um usuario"}, 401


@jwt_required()
def listar_usuarios():
  usuarios = (UsuarioModel.query.all())

  lista_usuarios = [usuarios.serialize() for usuarios in usuarios]

  return jsonify(lista_usuarios), 200


@jwt_required()
def listar_usuario_id(usuario_id: int):
  try:
    usuario = UsuarioModel.query.filter_by(id=usuario_id).first()

    return jsonify(usuario.serialize()), 200
  except AttributeError:
    return {"error": "Usuario não existe."}, 404


@jwt_required()
def atualizar_senha():
  session = current_app.db.session
  data = request.get_json()
  current_user = get_jwt_identity()

  try:
    verificar_usuario(current_user)
    usuario = UsuarioModel.query.get(current_user)
    for k in data.keys():
        if k != "password":
            return {"error": "Chaves aceitas: [password]"}, 409

    data["updated_at"] = datetime.now()

    for k, v in data.items():
      setattr(usuario, k, v)

    session.add(usuario)
    session.commit()
    
    return {"msg": "Senha atualizada"}, 200
  except NaoUsuarioError:
    return {"error": "Você não esta logado como um usuario"}, 401


@jwt_required()
def simulaçao_frete():
  data: dict = request.get_json()
  current_user = get_jwt_identity()

  try:
    verificar_usuario(current_user)
    
    chaves_validas = ['origem', 'destino', 'codigo_uf_origem', 'codigo_uf_destino', 'volume']
    chaves_invalidas = []
    for k in data.keys():
      if k not in chaves_validas:
        chaves_invalidas.append(k)
    if len(chaves_invalidas) > 0:
      return {"error": {"chaves invalidas": chaves_invalidas}}
    
    origem = data['origem']
    destino = data['destino']
    codigo_uf_origem = data['codigo_uf_origem']
    codigo_uf_destino = data['codigo_uf_destino']
    volume = data['volume']

    coords_origem = gerar_latitude_longitude(origem, codigo_uf_origem)
    coords_destino = gerar_latitude_longitude(destino, codigo_uf_destino) 

    valor = calcular_frete(coords_origem, coords_destino, volume)
    previsão_entrega = calcular_previsão_de_entrega(coords_origem, coords_destino, datetime.now())

    serializer ={
      "dados simulados": 
          {
            "valor": valor,
            "previsão de entrega": previsão_entrega 
          }
    }

    return jsonify(serializer), 200

  except NaoUsuarioError:
    return {"error": "Você não está logado como usuario"}
  except AttributeError:
    return {"error": "Nome de cidade ou codigo uf estão errados"}, 404