from flask import request, current_app
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity
from app.exceptions.exc import NaoUsuarioError, NotaInvalidaError
from app.models.avaliacao_usuario_motorista_model import AvaliacaoUsuarioMotoristaModel
from sqlalchemy.exc import IntegrityError

@jwt_required()
def avaliar_usuario():
  try:
    session = current_app.db.session
    current_user = get_jwt_identity()
    data = request.get_json()
    nota = data['nota']
    if nota > 5 or nota < 0:
      raise NotaInvalidaError

    if type(current_user) == int:
      try:
        avaliacao = AvaliacaoUsuarioMotoristaModel.query.filter_by(motorista_id=data['motorista_id']).first()
        nota_atual = avaliacao.nota
        if nota_atual == 0:
          nova_nota = nota
        else:
          nova_nota = (nota_atual + nota) / 2
        setattr(avaliacao, 'nota', nova_nota)
        
        session.commit()

        return {'msg': "Nota alterada com sucesso"}, 200
      except KeyError:
        return {"error": "Você não esta logado como Motorista"}, 401
    
    elif type(current_user) == dict:
      try:
        avaliacao = AvaliacaoUsuarioMotoristaModel.query.filter_by(usuario_id=data['usuario_id']).first()
        nota_atual = avaliacao.nota
        if nota_atual == 0:
          nova_nota = nota
        else:
          nova_nota = (nota_atual + nota) / 2

        nova_nota = round(nova_nota, 1)
        setattr(avaliacao, 'nota', nova_nota)     
        session.commit()

        return {'msg': "Nota alterada com sucesso"}, 200
      except KeyError:
        return {"error": "Você não esta logado como Usuario"}, 401

  except IntegrityError:
    return {"error": "Usuário já foi desativado"}, 409
  except AttributeError:
    return {"error": "Este usuario não existe."}, 404
  except NotaInvalidaError:
    return {"error": "Avaliações maiores que 5 e menores que 0 são invalidas"}, 400
    