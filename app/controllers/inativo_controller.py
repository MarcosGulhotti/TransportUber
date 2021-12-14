from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required
from app.models.motorista_model import MotoristaModel
from app.models.usuario_inativo_model import UsuarioInativoModel
from app.models.usuario_model import UsuarioModel
from sqlalchemy.exc import IntegrityError

@jwt_required()
def desativar_usuario():
  try:
    session = current_app.db.session
    data = request.get_json()

    if 'motorista_id' in data.keys():

      usuario: MotoristaModel = MotoristaModel.query.filter_by(id=data['motorista_id']).first()
      setattr(usuario, 'motorista_ativo', False)

      novo_inativo = UsuarioInativoModel(**data)
      session.add(novo_inativo)   

    elif 'usuario_id' in data.keys():

      usuario: UsuarioModel = UsuarioModel.query.filter_by(id=data['usuario_id']).first()
      setattr(usuario, 'usuario_ativo', False)

      novo_inativo = UsuarioInativoModel(**data)
      session.add(novo_inativo)

    session.commit()

    return jsonify(novo_inativo), 201

  except IntegrityError:
    return {"error": "Usuário ou Motorista já foi desativado."}, 409
  except AttributeError:
     return {"error": "Usuário ou Motorista não existe."}, 409
            
