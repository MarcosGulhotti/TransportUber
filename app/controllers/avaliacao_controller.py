from flask import request, current_app
from flask_jwt_extended import jwt_required
from app.exceptions.exc import NotaInvalidaError
from app.models.avaliacao_usuario_motorista_model import AvaliacaoUsuarioMotoristaModel
from sqlalchemy.exc import IntegrityError

@jwt_required()
def avaliar_usuario():
  try:
    session = current_app.db.session
    data = request.get_json()
    nota = data['nota']
    if nota > 5 or nota < 0:
      raise NotaInvalidaError

    if 'motorista_id' in data.keys():
      avaliacao = AvaliacaoUsuarioMotoristaModel.query.filter_by(motorista_id=data['motorista_id']).first()
      nota_atual = avaliacao.nota
      if nota_atual == 0:
        nova_nota = nota
      else:
        nova_nota = (nota_atual + nota) / 2
      setattr(avaliacao, 'nota', nova_nota)   

    elif 'usuario_id' in data.keys():
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

  except IntegrityError:
    return {"error": "Usuário já foi desativado"}, 409
  except AttributeError:
    return {"error": "Este usuario não existe."}, 404
  except NotaInvalidaError:
    return {"error": "Avaliações maiores que 5 e menores que 0 são invalidas"}, 400
    