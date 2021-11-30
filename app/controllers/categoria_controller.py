from flask import request, jsonify, current_app
from app.models.categoria_model import CategoriaModel

def criar_categoria():
  session = current_app.db.session
  data = request.get_json()

  nova_categoria = CategoriaModel(**data)

  session.add(nova_categoria)
  session.commit()

  return jsonify(nova_categoria.serialize()), 201