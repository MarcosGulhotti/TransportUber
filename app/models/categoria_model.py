from sqlalchemy.orm import relationship
from app.models.carga_categoria_table import cargas_categorias
from app.configs.database import db
from sqlalchemy import Column, Integer, String
from dataclasses import dataclass

from app.models.carga_model import CargaModel

@dataclass
class CategoriaModel(db.Model):
  nome: str
  cargas: CargaModel

  __tablename__ = 'categorias'

  id = Column(Integer, primary_key=True)
  nome = Column(String, nullable=False)

  cargas = relationship('CargaModel', secondary=cargas_categorias, backref='categorias')

  def serialize(self):
    return {
      'nome': self.nome,
      'cargas': self.cargas
    }