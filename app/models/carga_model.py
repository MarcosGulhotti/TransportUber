from sqlalchemy.orm import backref, relationship, validates
import re
from app.configs.database import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from dataclasses import dataclass
from app.models.caminhao_model import CaminhaoModel
from app.exceptions.exc import PrevisaoEntregaFormatError

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

  __tablename__ = 'cargas'

  id = Column(Integer, primary_key=True)
  disponivel = Column(Boolean, nullable=False, default=True)
  descricao = Column(String)
  destino = Column(String)
  origem = Column(String, nullable=False)
  horario_saida = Column(DateTime)
  horario_chegada = Column(DateTime)
  previsao_entrega = Column(String)
  volume = Column(Float, nullable=False)
  caminhao_id = Column(Integer, ForeignKey('caminhoes.id'))
  dono_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

  caminhao = relationship('CaminhaoModel', backref=backref('carga', uselist=False), uselist=False)
  
  @validates('previsao_entrega')
  def valida_previsao_entrega(self, key, previsao_entrega):
    pattern = "(^\d{2}\/\d{2}\/\d{4}$)"

    if not re.search(pattern, previsao_entrega):
      raise PrevisaoEntregaFormatError("Formato para previsão de entrega inválido. Formato aceito = xx/xx/xxxx")

    return previsao_entrega

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
      'categorias': [categoria.nome for categoria in self.categorias]
    }