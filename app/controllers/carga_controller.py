from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app.models.carga_model import CargaModel
from app.models.categoria_model import CategoriaModel
from werkzeug.exceptions import NotFound

@jwt_required()
def criar_carga(dono_id: int):
  session = current_app.db.session
  data = request.get_json()

  data['dono_id'] = dono_id

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


def listar_carga(carga_id: int):
  carga = CargaModel.query.get(carga_id)

  return jsonify(carga.serialize()), 200


def listar_carga_id(carga_id: int):
  try:
    carga = CargaModel.query.filter_by(id=carga_id).first()
    return jsonify(carga.serialize())
  except AttributeError:
    return {"error": f"Carga de id {carga_id} não existe"}, 400
    

def listar_carga_origem(origem):
  try:
    carga = CargaModel.query.filter_by(origem=origem).all()
    lista_cargas = [cargas.serialize() for cargas in carga]
    return jsonify(lista_cargas)
  except AttributeError:
    return {"error": "Carga não foi encontrada"}, 400


def listar_carga_destino(destino):
  try:
    carga = CargaModel.query.filter_by(destino=destino).all()
    lista_cargas = [cargas.serialize() for cargas in carga]
    return jsonify(lista_cargas)
  except AttributeError:
    return {"error": "Carga não foi encontrada"}, 400

def atualizar_disponivel(carga_id: int):
  try:
    session = current_app.db.session
    carga = CargaModel.query.get(carga_id)

    setattr(carga, "disponivel", not carga.disponivel)
    session.add(carga)
    session.commit()

    return carga.serialize()
  except KeyError as e:
    return {"error": f"Chave(s) faltantes {e.args}"}, 400

def atualizar_carga(carga_id: int):
  try:
    session = current_app.db.session
    carga = CargaModel.query.get(carga_id)
    data = request.get_json()

    if carga.disponivel == False:
      for k in data.keys():
        if k != "previsao_entrega":
            return {"error": "Chaves aceitas: [previsao_entrega]"}, 409

      nova_previsao = data["previsao_entrega"]
      setattr(carga, "previsao_entrega", nova_previsao)
      return carga.serialize()


    colunas_invalidas = ["id", "dono", "caminhao", "disponivel"]
    for k, v in data.items():
      if k not in colunas_invalidas:
        setattr(carga, k, v)
      else:
        return {"error": f"Chave inválida: ({k})"}, 409

    session.add(carga)
    session.commit()

    return carga.serialize()
  except KeyError as e:
    return {"error": f"Chave(s) faltantes {e.args}"}, 400
