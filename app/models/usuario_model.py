from sqlalchemy.orm import relationship, validates
from app.configs.database import db
from sqlalchemy import Column, Integer, String, DateTime
import re
from app.exceptions.exc import CpfFormatError, CelularFormatError
from dataclasses import dataclass
from app.models.carga_model import CargaModel
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class UsuarioModel(db.Model):
  nome: str
  sobrenome: str
  cpf: str
  created_at: str
  email: str
  celular: str
  updated_at: str
  cargas: CargaModel

  __tablename__ = 'usuarios'
  
  id = Column(Integer, primary_key=True)
  nome = Column(String, nullable=False)
  sobrenome = Column(String, nullable=False)
  password_hash = Column(String(255), nullable=False)
  cpf = Column(String, nullable=False, unique=True)
  created_at = Column(DateTime)
  email = Column(String)
  celular = Column(String, nullable=False)
  updated_at = Column(DateTime)

  cargas = relationship('CargaModel', backref='dono', uselist=False)

  @validates('cpf')
  def valida_cpf(self, key, cpf):
    pattern_cpf = "(^\d{3}\.\d{3}\.\d{3}\-\d{2}$)"

    if not re.search(pattern_cpf, cpf):
      raise CpfFormatError("Formato de CPF inválido. Formato aceito = xxx.xxx.xxx-xx")

    return cpf
  
  @validates('celular')
  def valida_celular(self, key, celular):
    pattern_celular = "^\([1-9]{2}\)(?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$"

    if not re.search(pattern_celular, celular):
      raise CelularFormatError("Formato de celular inválido. Formato aceito = (xx)xxxxx-xxxx")
    
    return celular
  
  @property
  def password(self):
    raise AttributeError("Password cannot be acessed!")
  
  @password.setter
  def password(self, password_to_hash):
    self.password_hash = generate_password_hash(password_to_hash)
  
  def verify_password(self, password_to_compare):
    return check_password_hash(self.password_hash, password_to_compare)