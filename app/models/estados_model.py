from app.configs.database import db
from sqlalchemy import Column, Integer, String
from dataclasses import dataclass

@dataclass
class EstadoModel(db.Model):
  id: int
  nome: str
  codigo_uf: int
  uf: str

  __tablename__ = 'estados'

  id = Column(Integer, primary_key=True)
  nome = Column(String, nullable=False)
  codigo_uf = Column(Integer, nullable=False)
  uf = Column(String, nullable=False)

  def serialize(self):
    return{
      "id": self.id,
      "nome": self.nome,
      "codigo_uf": self.codigo_uf,
      "uf": self.uf
    }