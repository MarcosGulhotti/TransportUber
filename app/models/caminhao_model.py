from sqlalchemy.orm import validates
import re
from app.configs.database import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from dataclasses import dataclass
from app.exceptions.exc import PlacaFormatError

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

  @validates('placa')
  def valida_placa(self, key, placa):
    pattern_default = "(^[a-zA-Z]{3}\-[0-9]{4}$)"
    pattern_mercosul = "(^[a-zA-Z]{3}[0-9][A-Za-z0-9][0-9]{2}$)"

    if not re.search(pattern_default, placa) or re.search(pattern_mercosul, placa):
      raise PlacaFormatError("Formato para placa inválido. Formatos aceitos = ZZZ-9999 ou ZZZ9Z99 (Mercosul).")

    return placa
  
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