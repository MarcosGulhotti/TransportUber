from datetime import timedelta, datetime
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.exceptions.exc import CategoryTypeError, RequiredKeysError,PrevisaoEntregaFormatError
from app.models.carga_model import CargaModel
from app.models.categoria_model import CategoriaModel
from werkzeug.exceptions import NotFound
from haversine import haversine

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

  return total

@jwt_required()
def criar_carga():
  session = current_app.db.session
  data = request.get_json()
  current_user = get_jwt_identity()
  
  try:
    data['dono_id'] = current_user
    valor_frete = calcular_frete(
      origem=data["origem"],
      destino=data["destino"],
      volume=data["volume"]
    )
    data["valor_frete"] = valor_frete
    data["valor_frete_motorista"] = valor_frete - (valor_frete*0.3)

    chaves_necessarias = ['disponivel', 'destino', 'origem', 'volume', 'descricao', 'categorias', ]
    for key in chaves_necessarias:
      if key not in data:
        raise RequiredKeysError(f'Está faltando a chave ({key}).')
    
    chaves_model = ['disponivel', 'destino', 'origem', 'volume', 'descricao', 'categorias', 'dono_id', 'valor_frete', 'valor_frete_motorista']
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
  previsão = km / media_kmh
  previsão = previsão.__round__(2)
  data_chegada = horario_saida + timedelta(hours=previsão)

  data_chegada = data_chegada.strftime('%d/%m/%Y')


  return f"{data_chegada}"

@jwt_required()
def atualizar_disponivel(carga_id: int):  
  try:
    session = current_app.db.session
    carga = CargaModel.query.get(carga_id)

    setattr(carga, 'horario_saida', datetime.now())
    setattr(carga, "disponivel", not carga.disponivel)

    previsão_entrega = calcular_previsão_de_entrega(carga.origem, carga.destino, datetime.now())

    setattr(carga, "previsao_entrega", previsão_entrega)
    session.add(carga)
    session.commit()

    return carga.serialize()
  except KeyError as e:
    return {"msg": f"Chave(s) faltantes {e.args}."}, 400
  except AttributeError:
    return jsonify({"msg": "Carga não existe."}), 404

@jwt_required()
def deletar_carga(carga_id):
  try:
    carga_deletada = CargaModel.query.filter_by(
      id=carga_id).first_or_404(description="Carga não encontrada")
    current_app.db.session.delete(carga_deletada)
    current_app.db.session.commit()
    return "", 204
  except NotFound:
    return jsonify({"msg": "Carga não existe."}), 404


@jwt_required()
def atualizar_carga(carga_id: int):
  try:
    session = current_app.db.session
    carga = CargaModel.query.get(carga_id)
    data = request.get_json()

    if carga.disponivel == False:
      for k in data.keys():
        if k != "previsao_entrega":
            return {"msg": "Chaves aceitas: [previsao_entrega]."}, 409

      nova_previsao = data["previsao_entrega"]
      setattr(carga, "previsao_entrega", nova_previsao)
      return carga.serialize()

    # colunas = [
    #   "descricao", "destino", "origem", "horario_saida", "horario_chegada", "previsao_entrega", "volume"
    #   ]
    
    # valor_frete = calcular_frete(
    #   origem=carga.origem,
    #   destino=carga.destino,
    #   volume=carga.volume
    # )
    # carga.valor_frete = valor_frete
    # carga.valor_frete_motorista = valor_frete - (valor_frete*0.3)

    # for k, v in data.items():
    #   if k in colunas:
    #     setattr(carga, k, v)
    #   else:
    #     raise KeyError(k)

    # session.add(carga)
    # session.commit()

    # return carga.serialize()
  except KeyError as e:
    return {"msg": f"Chave(s) desnecessária(s) ou não é permitida a atualização: {e.args}."}, 400
  except PrevisaoEntregaFormatError as e:
    return {'msg': str(e)}, 400
  except AttributeError:
    return jsonify({"msg": "Carga não existe."}), 404