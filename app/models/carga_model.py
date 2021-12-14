from sqlalchemy.orm import backref, relationship
from app.configs.database import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from dataclasses import dataclass
from app.models.caminhao_model import CaminhaoModel

@dataclass
class CargaModel(db.Model):
  id: int
  disponivel: bool
  descricao: str
  destino: str
  origem: str
  horario_saida: str
  horario_chegada: str
  volume: float
  caminhao: CaminhaoModel
  valor_frete: float
  valor_frete_motorista: float

  __tablename__ = 'cargas'

  id = Column(Integer, primary_key=True)
  disponivel = Column(Boolean, nullable=False, default=True)
  descricao = Column(String)
  destino = Column(String)
  origem = Column(String, nullable=False)
  horario_saida = Column(DateTime)
  horario_chegada = Column(DateTime)
  previsao_entrega = Column(DateTime)
  volume = Column(Float, nullable=False)
  caminhao_id = Column(Integer, ForeignKey('caminhoes.id'))
  dono_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
  valor_frete = Column(Float, nullable=False)
  valor_frete_motorista = Column(Float, nullable=False)


  caminhao = relationship('CaminhaoModel', backref=backref('carga', uselist=False), uselist=False)

  def serialize(self):
    return {
      'id': self.id,
      'disponivel': self.disponivel,
      'descricao': self.descricao,
      'destino': self.destino,
      'origem': self.origem,
      'horario_saida': self.horario_saida,
      'horario_chegada': self.horario_chegada,
      'previsao_entrega': self.previsao_entrega,
      'volume': self.volume,
      'caminhao': self.caminhao,
      'dono': f'{self.dono.nome} {self.dono.sobrenome}',
      'categorias': [categoria.nome for categoria in self.categorias],
      "valor_frete": round(self.valor_frete, 2),
      "valor_frete_motorista": round(self.valor_frete_motorista, 2)
    }