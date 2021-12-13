from flask import Flask
from app.routes.usuario_blueprint import bp_usuario
from app.routes.motorista_blueprint import bp_motorista
from app.routes.categoria_blueprint import bp_categoria
from app.routes.autorização_blueprint import bp_autenticacao

def init_app(app: Flask):
  app.register_blueprint(bp_usuario)
  app.register_blueprint(bp_motorista)
  app.register_blueprint(bp_categoria)
  app.register_blueprint(bp_autenticacao)