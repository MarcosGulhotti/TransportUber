from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey
from dataclasses import dataclass
from app.models.caminhao_model import CaminhaoModel
from app.models.carga_model import CargaModel
from app.models.motorista_model import MotoristaModel
from app.models.usuario_model import UsuarioModel
# from app.models.motorista_model import MotoristaModel
# from app.models.usuario_model import UsuarioModel

@dataclass
class EntregaRealizadaModel(db.Model):
  id: int
  carga_id: CargaModel

  __tablename__ = 'entregas_realizadas'

  id = Column(Integer, primary_key=True)
  carga_id = Column(Integer, ForeignKey('cargas.id'), unique=True)
  # motorista_id = Column(Integer, ForeignKey('motoristas.id'), unique=True)
  # dono_id = Column(Integer, ForeignKey('usuarios.id'), unique=True)

  def serialize(self):
    carga = CargaModel.query.get(self.carga_id)
    dono = UsuarioModel.query.get(carga.dono_id)
    caminhão = CaminhaoModel.query.get(carga.caminhao_id)
    motorista = MotoristaModel.query.get(caminhão.motorista_id)
    return {
      "data": [{
          "id": self.id,
          "Carga": carga, 
          "Dono":  {
            "id": dono.id,
            "nome": f'{dono.nome} {dono.sobrenome}',
          },
          "Motorista": {
            "id": caminhão.motorista_id,
            "nome": f'{motorista.nome} {motorista.sobrenome}'
          }
        }]
    }
