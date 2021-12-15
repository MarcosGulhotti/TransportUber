from flask_jwt_extended.view_decorators import jwt_required
from app.models.municipios_model import MunicipioModel
from haversine import haversine
from datetime import timedelta

def calcular_frete(origem, destino, volume):
  """
  Função para calcular o frete de uma carga baseado em sua origem,\n
  destino e algumas taxas do aplicativo

  origem => "{latitude}, {longitude}"

  destino => "{latitude}, {longitude}"

  taxa/km => R$1.20

  taxa/m3 => R$120
  """

  origem = tuple([float(x) for x in origem.split(",")])
  destino = tuple([float(x) for x in destino.split(",")])

  km = haversine(origem, destino)
  total = (km*1.20) + (volume*120)
  total = round(total, 2)

  return total

def gerar_latitude_longitude(cidade, codigo_uf):
  """
  Função para gerar latitude e longitude baseada na cidade e seu código uf

  cidade => String

  codigo_uf => Integer
  """

  cidade = cidade.lower()
  municipio: MunicipioModel = MunicipioModel.query.filter_by(nome=cidade, codigo_uf=codigo_uf).first()
  
  return f'{municipio.latitude}, {municipio.longitude}'


def calcular_previsão_de_entrega(origem, destino, horario_saida):
  """
  Função para calcular a previsão de entrega baseada em variaveis tais como:

  km em linha reta do ponto de origem até o destino \n
  media de velocidade de caminhões em rodovias (80kmh)\n
  horas trabalhadas diariamente por caminhoneiros (10 horas)\n
  30% de atraso devido a rotas instaveis\n
  5% de atraso como coeficiente para possiveis imprevistos na estrada
  """
  origem = tuple([float(x) for x in origem.split(",")])
  destino = tuple([float(x) for x in destino.split(",")])

  km = haversine(origem, destino)
  media_kmh = 80
  horas_trabalhadas = 10
  new_km = km * 1.3
  previsão = new_km / (media_kmh * (horas_trabalhadas * 1.05))
  previsão = previsão * 24
    
  data_chegada = horario_saida + timedelta(hours=previsão)

  if data_chegada.hour > 18 or data_chegada.hour < 8:
    if data_chegada.hour > 18:
      time = 24 - data_chegada.hour
    elif data_chegada.hour < 8:
      time = 8 - data_chegada.hour
  else:
    time = data_chegada.hour
    
  data_chegada = data_chegada + timedelta(hours=time)

  return data_chegada
