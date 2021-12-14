from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app: Flask):
  db.init_app(app)
  app.db = db

  from app.models.caminhao_model import CaminhaoModel
  from app.models.carga_model import CargaModel
  from app.models.motorista_model import MotoristaModel
  from app.models.usuario_model import UsuarioModel
  from app.models.categoria_model import CategoriaModel
  from app.models.avaliacao_usuario_motorista_model import AvaliacaoUsuarioMotoristaModel
  from app.models.entrega_realizada_model import EntregaRealizadaModel
  from app.models.municipios_model import MunicipioModel