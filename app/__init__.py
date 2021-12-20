from flask import Flask
from environs import Env
from app.configs import database, migrations
from app import routes
from flask_jwt_extended import JWTManager
from flask_cors import CORS

env = Env()
env.read_env()

def create_app():
  app = Flask(__name__)

  app.config["SQLALCHEMY_DATABASE_URI"] = env("SQLALCHEMY_DATABASE_URI")
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  app.config["JSON_SORT_KEYS"] = False
  app.config["JWT_SECRET_KEY"] = env("CHAVE_SECRETA")
  app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

  JWTManager(app)
  database.init_app(app)
  migrations.init_app(app)
  routes.init_app(app)
  CORS(app)

  return app
