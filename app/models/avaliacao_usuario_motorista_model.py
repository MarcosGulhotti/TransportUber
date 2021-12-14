from app.configs.database import db
from sqlalchemy import Column, Integer, Float, ForeignKey
from dataclasses import dataclass
from app.models.motorista_model import MotoristaModel
from app.models.usuario_model import UsuarioModel

@dataclass
class AvaliacaoUsuarioMotoristaModel(db.Model):
  id: int
  nota: float
  motorista_id: MotoristaModel
  usuario_id: UsuarioModel

  __tablename__ = 'avaliacoes_usuario_motorista'

  id = Column(Integer, primary_key=True)
  nota = Column(Float, nullable=False, default=0)
  motorista_id = Column(Integer, ForeignKey('motoristas.id'), unique=True)
  usuario_id = Column(Integer, ForeignKey('usuarios.id'), unique=True)
