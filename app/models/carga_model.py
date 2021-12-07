from sqlalchemy.orm import backref, relationship
from app.configs.database import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from dataclasses import dataclass
from app.models.caminhao_model import CaminhaoModel

@dataclass
class CargaModel(db.Model):
  id: int
  disponivel: bool
  destino: str
  origem: str
  horario_saida: str
  horario_chegada: str
  volume: float
  caminhao: CaminhaoModel

  __tablename__ = 'cargas'

  id = Column(Integer, primary_key=True)
  disponivel = Column(Boolean, nullable=False, default=True)
  destino = Column(String, nullable=False)
  origem = Column(String, nullable=False)
  horario_saida = Column(DateTime)
  horario_chegada = Column(DateTime)
  previsao_entrega = Column(String)
  volume = Column(Float, nullable=False)
  caminhao_id = Column(Integer, ForeignKey('caminhoes.id'))
  dono_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

  caminhao = relationship('CaminhaoModel', backref=backref('carga', uselist=False), uselist=False)
  
  def serialize(self):
    return {
      'id': self.id,
      'disponivel': self.disponivel,
      'destino': self.destino,
      'origem': self.origem,
      'horario_saida': self.horario_saida,
      'horario_chegada': self.horario_chegada,
      'previsao_entrega': self.previsao_entrega,
      'volume': self.volume,
      'caminhao': self.caminhao,
      'dono': f'{self.dono.nome} {self.dono.sobrenome}',
      'categorias': [categoria.nome for categoria in self.categorias]
    }