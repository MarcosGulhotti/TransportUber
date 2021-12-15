from datetime import timedelta, datetime
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import sqlalchemy
from app.controllers.helpers import paginar_dados
from app.exceptions.exc import CategoryTypeError, NaoMotoristaError, NaoUsuarioError, RequiredKeysError,PrevisaoEntregaFormatError, EntregaNãoEstaEmMovimentoError
from app.models.carga_model import CargaModel
from app.models.categoria_model import CategoriaModel
from werkzeug.exceptions import NotFound
from haversine import haversine
from app.models.entrega_realizada_model import EntregaRealizadaModel
from app.models.municipios_model import MunicipioModel

def calcular_frete(origem, destino, volume):
  """
  origem => "{latitude}, {longitude}"
  destino => "{latitude}, {longitude}"
  taxa/km => R$1.20
  taxa/m3 => R$120
  """

  origem = tuple([float(x) for x in origem.split(",")])
  destino = tuple([float(x) for x in destino.split(",")])

  km = haversine(origem, destino)
  total = (km*1.20) + (volume*120)
  total = round(total, 2)

  return total

def gerar_latitude_longitude(cidade, codigo_uf):
  cidade = cidade.lower()
  municipio: MunicipioModel = MunicipioModel.query.filter_by(nome=cidade, codigo_uf=codigo_uf).first()
  
  return f'{municipio.latitude}, {municipio.longitude}'

@jwt_required()
def criar_carga():
  session = current_app.db.session
  data = request.get_json()
  current_user = get_jwt_identity()
  
  try:
    if type(current_user) == dict:
      raise NaoUsuarioError
    data['destino'] = data['destino'].lower()
    data['origem'] = data['origem'].lower()
    data['dono_id'] = current_user

    try:
      coord_origem = gerar_latitude_longitude(data['origem'], data['codigo_uf_origem'])
    except AttributeError:
      return {'error': 'Origem ou codigo_UF não existem.'}, 404
    try:
      coord_destino = gerar_latitude_longitude(data['destino'], data['codigo_uf_destino'])
    except AttributeError:
      return {'error': 'Destino ou codigo_UF não existem.'}, 404

    valor_frete = calcular_frete(
      origem=coord_origem,
      destino=coord_destino,
      volume=data["volume"]
    )
    data["valor_frete"] = valor_frete
    data["valor_frete_motorista"] = valor_frete - (valor_frete*0.3)

    chaves_necessarias = ['disponivel', 'destino', 'origem', 'volume', 'descricao', 'categorias', 'codigo_uf_origem', 'codigo_uf_destino' ]
    for key in chaves_necessarias:
      if key not in data:
        raise RequiredKeysError(f'Está faltando a chave ({key}).')

    chaves_model = ['disponivel', 'destino', 'origem', 'volume', 'descricao', 'categorias', 'dono_id', 'valor_frete', 'valor_frete_motorista', 'codigo_uf_origem', 'codigo_uf_destino' ]
    for key in data:
      if key not in chaves_model:
        raise RequiredKeysError(f'A chave ({key}) não é necessária.')
    
    if type(data['categorias']) != list or type(data['volume']) != float:
      raise CategoryTypeError(data['categorias'], data['volume'])
    
    categorias = data.pop('categorias')

    nova_carga = CargaModel(**data)

    for categoria in categorias:
      nova_categoria = CategoriaModel.query.filter_by(nome=categoria["nome"]).first()
      if not nova_categoria:
        nova_categoria = CategoriaModel(**categoria)
        session.add(nova_categoria)
        session.commit()

      nova_carga.categorias.append(nova_categoria)
    
    session.add(nova_carga)
    session.commit()

    return jsonify(nova_carga.serialize()), 201
  
  except RequiredKeysError as e:
    return {'msg': str(e)}, 400
  except CategoryTypeError as e:
    return e.message, 400
  except NaoUsuarioError:
    return {"error": "Você não está logado como um usuario"}, 401


@jwt_required()
def listar_carga_id(carga_id: int):
  try:
    carga = CargaModel.query.get(carga_id)

    return jsonify(carga.serialize()), 200
  except AttributeError:
    return {"msg": f"Carga de id {carga_id} não existe."}, 400

    
@jwt_required()
def listar_carga_origem(origem):
  try:
    carga = CargaModel.query.filter_by(origem=origem).all()
    lista_cargas = [cargas.serialize() for cargas in carga]
    return jsonify(lista_cargas)
  except AttributeError:
    return {"msg": "Carga não foi encontrada."}, 400

@jwt_required()
def listar_carga_destino(destino):
  try:
    carga = CargaModel.query.filter_by(destino=destino).all()
    lista_cargas = [cargas.serialize() for cargas in carga]
    return jsonify(lista_cargas)
  except AttributeError:
    return {"msg": "Carga não foi encontrada."}, 400

def calcular_previsão_de_entrega(origem, destino, horario_saida):
  origem = tuple([float(x) for x in origem.split(",")])
  destino = tuple([float(x) for x in destino.split(",")])

  km = haversine(origem, destino)
  media_kmh = 80
  horas_trabalhadas = 10
  new_km = km * 1.3
  previsão = new_km / (media_kmh * (horas_trabalhadas * 1.05))
  previsão = previsão * 24
    
  data_chegada = horario_saida + timedelta(hours=previsão)

  if data_chegada.hour > 18 or data_chegada.hour < 8:
    if data_chegada.hour > 18:
      time = 24 - data_chegada.hour
    elif data_chegada.hour < 8:
      time = 8 - data_chegada.hour
    
  data_chegada = data_chegada + timedelta(hours=time)

  return data_chegada

@jwt_required()
def pegar_carga(carga_id: int):  
  data = request.get_json()
  current_user = get_jwt_identity()
  try:
    if type(current_user) != dict:
      raise NaoMotoristaError
    session = current_app.db.session
    carga: CargaModel = CargaModel.query.get(carga_id)
    if carga.disponivel == False:
      return {"error": "Carga não disponivel"}, 401

    setattr(carga, 'horario_saida', datetime.now())
    setattr(carga, "disponivel", not carga.disponivel)
    setattr(carga, 'caminhao_id', data["caminhao_id"])

    coord_origem = gerar_latitude_longitude(carga.origem, carga.codigo_uf_origem)
    coord_destino = gerar_latitude_longitude(carga.destino, carga.codigo_uf_destino)

    previsão_entrega = calcular_previsão_de_entrega(coord_origem, coord_destino, datetime.now())

    setattr(carga, "previsao_entrega", previsão_entrega)
    session.add(carga)
    session.commit()

    return carga.serialize()
  except KeyError as e:
    return {"msg": f"Chave(s) faltantes {e.args}."}, 400
  except AttributeError:
    return jsonify({"msg": "Carga não existe."}), 404
  except sqlalchemy.exc.IntegrityError:
    return {"error": "caminhão não encontrado no banco"}, 404
  except NaoMotoristaError:
    return {"error": "Você não esta logado como motorista"}, 401

@jwt_required()
def deletar_carga(carga_id):
  current_user = get_jwt_identity()
  try:
    if type(current_user) == dict:
      raise NaoUsuarioError
    carga_deletada = CargaModel.query.filter_by(
      id=carga_id).first_or_404(description="Carga não encontrada")

    current_app.db.session.delete(carga_deletada)
    current_app.db.session.commit()
    return "", 204
  except NotFound:
    return jsonify({"msg": "Carga não existe."}), 404
  except NaoUsuarioError:
    return {"error": "Você não esta logado como um usuario"}, 401
  except sqlalchemy.exc.IntegrityError:
    return {"error": "Carga já foi entregue ao usuario"}, 401


@jwt_required()
def atualizar_carga(carga_id: int):
  try:
    session = current_app.db.session
    carga: CargaModel = CargaModel.query.get(carga_id)
    data = request.get_json()

    if carga.disponivel:
      colunas = ["descricao", "volume"]

      for k, v in data.items():
        if k in colunas:
          setattr(carga, k, v)
        else:
          raise KeyError(k)

      session.add(carga)
      session.commit()

    return carga.serialize()
  except KeyError as e:
    return {"msg": f"Chave(s) desnecessária(s) ou não é permitida a atualização: {e.args}."}, 400
  except PrevisaoEntregaFormatError as e:
    return {'msg': str(e)}, 400
  except AttributeError:
    return jsonify({"msg": "Carga não existe."}), 404

@jwt_required()
def confirmar_entrega(carga_id: int):
  session = current_app.db.session
  current_user = get_jwt_identity()
  try:
    if type(current_user) == dict:
      raise NaoUsuarioError
    data = {"carga_id": carga_id}

    carga: CargaModel = CargaModel.query.get(carga_id)

    if carga.disponivel == True:
      raise EntregaNãoEstaEmMovimentoError

    entrega_realizada = EntregaRealizadaModel(**data)
    session.add(entrega_realizada)
    session.commit()
  except sqlalchemy.exc.IntegrityError:
    return {"error": "carga não existe ou já foi entregue"}, 404
  except EntregaNãoEstaEmMovimentoError:
    return {"error": "Carga ainda não saiu para entrega"}, 404
  except NaoUsuarioError:
    return {"error": "Você não esta logado como um usuario"}, 401

  return {"msg": "Entrega da carga realizada com sucesso!!"}, 200

@jwt_required()
def listar_cargas_entregues():
  try:
    entregas_realizadas = EntregaRealizadaModel.query.all()
    serialize = [entrega.serialize() for entrega in entregas_realizadas]

    return jsonify(serialize), 200
  except AttributeError:
    return {'error': "Não existem cargas entregues."}, 404

def filtra_cargas(lista_query):
  try:
    lista_resultado = []

    cargas = CargaModel.query.all()
    cargas = [carga.serialize() for carga in cargas]

    for item in lista_query:
      chave = [*item.keys()][0]
      valor = [*item.values()][0]
      if chave.startswith("codigo"):
        valor = int(valor)
      for item in cargas:
        if item[chave] == valor:
          lista_resultado.append(item)
    
    return lista_resultado
  except KeyError as e:
    return f"Chave(s) desnecessária(s)/inválida(s): {e.args}."

@jwt_required()
def listar_cargas():
  data = request.args
  pagina, por_pagina = 1, 15

  for k, v in data.items():
    if k == "pagina":
      pagina = int(v)
    if k == "por_pagina":
      por_pagina = int(v)

  if len(data) == 0:
    cargas = CargaModel.query.all()
    cargas = [carga.serialize() for carga in cargas]
    return paginar_dados(dados=cargas, pagina=pagina, por_pagina=por_pagina)

  query_permitidas = ["origem", "destino", "disponivel", "codigo_uf_origem", "codigo_uf_destino"]

  filtros = [{k: v} for k,v in data.items() if k.lower() in query_permitidas]

  return paginar_dados(dados=filtra_cargas(filtros), pagina=pagina, por_pagina=por_pagina)


  