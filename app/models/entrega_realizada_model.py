from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey
from dataclasses import dataclass
from app.models.carga_model import CargaModel
# from app.models.motorista_model import MotoristaModel
# from app.models.usuario_model import UsuarioModel

@dataclass
class EntregaRealizadaModel(db.Model):
  id: int
  carga_id: CargaModel

  __tablename__ = 'entregas_realizadas'

  id = Column(Integer, primary_key=True)
  carga_id = Column(Integer, ForeignKey('cargas.id'), unique=True)
  # motorista_id = Column(Integer, ForeignKey('motoristas.id'), unique=True)
  # dono_id = Column(Integer, ForeignKey('usuarios.id'), unique=True)

