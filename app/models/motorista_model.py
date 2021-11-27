from sqlalchemy.orm import relationship, validates
from app.configs.database import db
from sqlalchemy import Column, Integer, String, DateTime
import re
from app.exceptions.exc import CpfFormatError

class MotoristaModel(db.Model):
  __tablename__ = 'motoristas'
  
  id = Column(Integer, primary_key=True)
  nome = Column(String, nullable=False)
  sobrenome = Column(String, nullable=False)
  cpf = Column(String, nullable=False, unique=True)
  created_at = Column(DateTime)
  
  caminhoes = relationship('CaminhaoModel', backref='motorista', uselist=False)

  @validates('cpf')
  def valida_cpf(self, key, cpf):
    pattern = "(^\d{3}\.\d{3}\.\d{3}\-\d{2}$)"

    if not re.search(pattern, cpf):
      raise CpfFormatError("Formato de CPF inválido. Formato aceito = xxx.xxx.xxx-xx")

    return cpf