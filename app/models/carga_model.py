from sqlalchemy.orm import backref, relationship
from app.configs.database import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime

class CargaModel(db.Model):
  __tablename__ = 'cargas'

  id = Column(Integer, primary_key=True)
  disponivel = Column(Boolean, nullable=False)
  destino = Column(String, nullable=False)
  origem = Column(String, nullable=False)
  horario_saida = Column(DateTime)
  horario_chegada = Column(DateTime)
  peso = Column(Float, nullable=False)
  caminhao_id = Column(Integer, ForeignKey('caminhoes.id'), nullable=False, unique=True)
  dono_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False, unique=True)
  caminhao = relationship('CaminhaoModel', backref=backref('carga', uselist=False), uselist=False)
  