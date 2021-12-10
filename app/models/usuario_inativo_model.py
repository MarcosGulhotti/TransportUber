from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey
# from dataclasses import dataclass
# from app.models.motorista_model import MotoristaModel

# from app.models.usuario_model import UsuarioModel

# @dataclass
class UsuarioInativoModel(db.Model):
  # usuario_id: UsuarioModel
  # motorista_id: MotoristaModel

  __tablename__ = 'usuarios_inativos'

  id = Column(Integer, primary_key=True)
  usuario_id = Column(Integer, ForeignKey('usuarios.id'))
  motorista_id = Column(Integer, ForeignKey('motoristas.id'))
