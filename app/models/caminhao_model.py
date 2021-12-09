from app.configs.database import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from dataclasses import dataclass

@dataclass
class CaminhaoModel(db.Model):
  marca: str
  modelo: str
  capacidade_de_carga: float
  placa: str

  __tablename__ = 'caminhoes'

  id = Column(Integer, primary_key=True)
  marca = Column(String, nullable=False)
  modelo = Column(String, nullable=False)
  capacidade_de_carga = Column(Float, nullable=False)
  placa = Column(String, nullable=False, unique=True)
  motorista_id = Column(Integer, ForeignKey('motoristas.id'), nullable=False)
  
  def serialize(self):
    return {
      'id': self.id,
      'marca': self.marca,
      'modelo': self.modelo,
      'capacidade_de_carga': self.capacidade_de_carga,
      'placa': self.placa,
      'motorista': {
        "nome": f'{self.motorista.nome} {self.motorista.sobrenome}',
        "CNH": self.motorista.cnh
        }
    }