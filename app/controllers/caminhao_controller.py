from flask import request, jsonify, current_app
from app.models.caminhao_model import CaminhaoModel
from app.models.motorista_model import MotoristaModel

def criar_caminhao():
  session = current_app.db.session
  data = request.get_json()

  data['marca'] = data['marca'].title()
  data['modelo'] = data['modelo'].title()
  id = data['motorista_id']

  motorista = MotoristaModel.query.get(id)

  novo_caminhao = CaminhaoModel(**data)

  session.add(novo_caminhao)
  session.commit()

  return jsonify({
    'marca': novo_caminhao.marca,
    'modelo': novo_caminhao.modelo,
    'capacidade_de_carga': novo_caminhao.capacidade_de_carga,
    'motorista': f"{motorista.nome} {motorista.sobrenome}"
  }), 201