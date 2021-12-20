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
  distancia_do_destino: float

  __tablename__ = 'cargas'

  id = Column(Integer, primary_key=True)
  disponivel = Column(Boolean, nullable=False, default=True)
  descricao = Column(String)
  destino = Column(String, nullable=False)
  codigo_uf_destino = Column(Integer, nullable=False)
  origem = Column(String, nullable=False)
  codigo_uf_origem = Column(Integer, nullable=False)
  horario_saida = Column(DateTime)
  horario_chegada = Column(DateTime)
  previsao_entrega = Column(DateTime)
  volume = Column(Float, nullable=False)
  caminhao_id = Column(Integer, ForeignKey('caminhoes.id'))
  dono_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
  valor_frete = Column(Float, nullable=False)
  valor_frete_motorista = Column(Float, nullable=False)
  distancia_do_destino = Column(Float)


  caminhao = relationship('CaminhaoModel', backref=backref('carga', uselist=False), uselist=False)

  def serialize(self):
    return {
      'id': self.id,
      'disponivel': self.disponivel,
      'descricao': self.descricao,
      'destino': self.destino.lower(),
      'codigo_uf_destino': self.codigo_uf_destino,
      'origem': self.origem.lower(),
      'codigo_uf_origem': self.codigo_uf_origem,
      'horario_saida': self.horario_saida,
      'horario_chegada': self.horario_chegada,
      'previsao_entrega': self.previsao_entrega,
      'volume': self.volume,
      'caminhao': self.caminhao,
      'dono': {
        "id": self.dono.id,  
        "nome": f'{self.dono.nome} {self.dono.sobrenome}'
      },
      'categorias': [categoria.nome for categoria in self.categorias],
      "valor_total_frete": round(self.valor_frete, 2),
      "valor_frete_motorista": round(self.valor_frete_motorista, 2),
      "distancia_do_destino": self.distancia_do_destino
    }