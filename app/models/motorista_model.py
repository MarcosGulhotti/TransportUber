from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql.sqltypes import Boolean, Float
from app.configs.database import db
from sqlalchemy import Column, Integer, String, DateTime
import re
from app.exceptions.exc import CelularFormatError, CpfFormatError
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.caminhao_model import CaminhaoModel

@dataclass
class MotoristaModel(db.Model):
  id: int
  nome: str
  sobrenome: str
  email: str
  celular: str
  cpf: str
  created_at: str
  cnh: str
  updated_at: str
  localizacao: str
  latitude: float
  longitude: float
  motorista_ativo: bool
  
  __tablename__ = 'motoristas'
  
  id = Column(Integer, primary_key=True)
  nome = Column(String, nullable=False)
  sobrenome = Column(String, nullable=False)
  email = Column(String, nullable=False, unique=True)
  celular = Column(String, nullable=False, unique=True)
  password_hash = Column(String(255), nullable=False)
  cpf = Column(String, nullable=False, unique=True)
  created_at = Column(DateTime)
  cnh = Column(String(11), nullable=False, unique=True)
  updated_at = Column(DateTime)
  localizacao = Column(String)
  motorista_ativo = Column(Boolean, default=True)
  latitude = Column(Float)
  longitude = Column(Float)

  caminhoes = relationship('CaminhaoModel', backref='motorista', uselist=False, cascade='all, delete-orphan')
  notas = relationship('AvaliacaoUsuarioMotoristaModel', backref='motorista', uselist=False, cascade='all, delete-orphan')
  
  @validates('cpf')
  def valida_cpf(self, key, cpf):
    pattern = "(^\d{3}\.\d{3}\.\d{3}\-\d{2}$)"

    if not re.search(pattern, cpf):
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


  def serialize(self):
    return {
      'id': self.id,
      'nome': self.nome,
      'sobrenome': self.sobrenome,
      'email': self.email,
      'celular': self.celular,
      'cpf': self.cpf,
      'cnh': self.cnh,
      'created_at': self.created_at,
      'updated_at': self.updated_at,
      'caminhoes': CaminhaoModel.query.filter_by(motorista_id=self.id).all(),
      'nota': self.notas.nota
    }