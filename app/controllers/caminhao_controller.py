from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app.models.caminhao_model import CaminhaoModel

@jwt_required()
def criar_caminhao(motorista_id: int):
  session = current_app.db.session
  data = request.get_json()

  data['marca'] = data['marca'].title()
  data['modelo'] = data['modelo'].title()
  data['motorista_id'] = motorista_id

  novo_caminhao = CaminhaoModel(**data)

  session.add(novo_caminhao)
  session.commit()

  return jsonify(novo_caminhao.serialize()), 201