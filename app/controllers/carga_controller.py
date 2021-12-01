from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app.models.carga_model import CargaModel
from app.models.categoria_model import CategoriaModel

@jwt_required()
def criar_carga(dono_id: int):
  session = current_app.db.session
  data = request.get_json()

  data['dono_id'] = dono_id

  categorias = data.pop('categorias')

  nova_carga = CargaModel(**data)

  for categoria in categorias:
    nova_categoria = CategoriaModel.query.filter_by(nome=categoria['nome']).first()
    
    if not nova_categoria:
      nova_categoria = CategoriaModel(**categoria)
      session.add(nova_categoria)
      session.commit()

    nova_carga.categorias.append(nova_categoria)

  session.add(nova_carga)
  session.commit()

  return jsonify(nova_carga.serialize()), 201