from app.configs.database import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from dataclasses import dataclass

@dataclass
class CaminhaoModel(db.Model):
  marca: str
  modelo: str
  capacidade_de_carga: float

  __tablename__ = 'caminhoes'

  id = Column(Integer, primary_key=True)
  marca = Column(String, nullable=False)
  modelo = Column(String, nullable=False)
  capacidade_de_carga = Column(Float, nullable=False)
  motorista_id = Column(Integer, ForeignKey('motoristas.id'), nullable=False)
  