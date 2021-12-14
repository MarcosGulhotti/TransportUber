from flask import request, jsonify, current_app
from flask_jwt_extended.utils import get_jwt_identity
from app.models.categoria_model import CategoriaModel
from werkzeug.exceptions import NotFound
from flask_jwt_extended import jwt_required
from app.models.usuario_model import UsuarioModel

@jwt_required()
def criar_categoria():
  current_user = get_jwt_identity()
  user = UsuarioModel.query.get(current_user)
  if user.super_adm:
    try:
      session = current_app.db.session
      data = request.get_json()

      nova_categoria = CategoriaModel(**data)

      session.add(nova_categoria)
      session.commit()

      return jsonify(nova_categoria.serialize()), 201
    
    except TypeError:
      return {'msg': 'É necessário passar a chave (nome).'}, 400
  else:
    return {"error": "Permissão insuficiente"}, 401


@jwt_required()
def deletar_categoria(categoria_id):
  current_user = get_jwt_identity()
  user = UsuarioModel.query.get(current_user)
  if user.super_adm:
    try:
      categoria_deletada = CategoriaModel.query.filter_by(
        id=categoria_id).first_or_404(description="Categoria não encontrada")

      current_app.db.session.delete(categoria_deletada)
      current_app.db.session.commit()

      return "", 204
    except NotFound:
      return jsonify({"erro": "Categoria não existe"}), 404  
  else:
    return {"error": "Permissão insuficiente"}, 401