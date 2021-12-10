from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.carga_model import CargaModel
from app.models.categoria_model import CategoriaModel
from werkzeug.exceptions import NotFound

@jwt_required()
def criar_carga():
  session = current_app.db.session
  data = request.get_json()
  current_user = get_jwt_identity()
  
  data['dono_id'] = current_user

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

@jwt_required()
def listar_carga(carga_id: int):
  carga = CargaModel.query.get(carga_id)

  return jsonify(carga.serialize()), 200

@jwt_required()
def listar_carga_id(carga_id: int):
  try:
    carga = CargaModel.query.filter_by(id=carga_id).first()
    return jsonify(carga.serialize())
  except AttributeError:
    return {"error": f"Carga de id {carga_id} não existe"}, 400
    
@jwt_required()
def listar_carga_origem(origem):
  try:
    carga = CargaModel.query.filter_by(origem=origem).all()
    lista_cargas = [cargas.serialize() for cargas in carga]
    return jsonify(lista_cargas)
  except AttributeError:
    return {"error": "Carga não foi encontrada"}, 400

@jwt_required()
def listar_carga_destino(destino):
  try:
    carga = CargaModel.query.filter_by(destino=destino).all()
    lista_cargas = [cargas.serialize() for cargas in carga]
    return jsonify(lista_cargas)
  except AttributeError:
    return {"error": "Carga não foi encontrada"}, 400

@jwt_required()
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

@jwt_required()
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


    colunas = [
      "descricao", "destino", "origem", "horario_saida", "horario_chegada", "previsao_entrega", "volume"
      ]
    
    for k, v in data.items():
      if k in colunas:
        setattr(carga, k, v)
      else:
        raise KeyError(k)

    session.add(carga)
    session.commit()

    return carga.serialize()
  except KeyError as e:
    return {"error": f"Chave(s) faltantes {e.args}"}, 400

@jwt_required()
def deletar_carga(carga_id):
  try:
    carga_deletada = CargaModel.query.filter_by(
      id=carga_id).first_or_404(description="Carga não encontrada")
    current_app.db.session.delete(carga_deletada)
    current_app.db.session.commit()
    return "", 204
  except NotFound:
    return jsonify({"erro": "Carga não existe"}), 404
