from sqlalchemy.orm import backref, relation, relationship
from sqlalchemy.sql.schema import ForeignKey
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


  def serialize(self):
    return{
      "id": self.id,
      "nome": self.nome,
      "codigo_uf": self.codigo_uf
    }