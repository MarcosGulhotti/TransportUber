from flask import request, jsonify, current_app
from app.models.categoria_model import CategoriaModel
from werkzeug.exceptions import NotFound
def criar_categoria():
  session = current_app.db.session
  data = request.get_json()

  nova_categoria = CategoriaModel(**data)

  session.add(nova_categoria)
  session.commit()

  return jsonify(nova_categoria.serialize()), 201


def deletar_categoria(categoria_id):
  try:
    categoria_deletada = CategoriaModel.query.filter_by(
      id=categoria_id).first_or_404(description="Categoria não encontrada")

    current_app.db.session.delete(categoria_deletada)
    current_app.db.session.commit()

    return "", 204
  except NotFound:
    return jsonify({"erro": "Categoria não existe"}), 404  