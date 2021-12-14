from app.configs.database import db
from sqlalchemy import Column, Integer, String
from dataclasses import dataclass

@dataclass
class MunicipioModel(db.Model):
  id: int
  nome: str
  latitude: str
  longitude: str
  codigo_uf: int

  __tablename__ = 'municipios'

  id = Column(Integer, primary_key=True)
  nome = Column(String, nullable=False)
  latitude = Column(String, nullable=False)
  longitude = Column(String, nullable=False)
  codigo_uf = Column(Integer, nullable=False)