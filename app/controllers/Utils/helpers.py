import math

from flask_jwt_extended.utils import get_jwt_identity
from app.exceptions.exc import MotoristaNaoVinculadoError

from app.models.carga_model import CargaModel
from app.models.motorista_model import MotoristaModel


def paginar_dados(dados, pagina = 1, por_pagina = 15):
    pagina = int(pagina)
    por_pagina = int(por_pagina)
    proxima, anterior = "", ""
    inicio = 0

    ultima_pagina = math.ceil(len(dados) / por_pagina)

    if pagina > ultima_pagina:
        pagina = ultima_pagina

    inicio = (pagina-1) * por_pagina
    fim = inicio + por_pagina
    dados_pagina = dados[inicio:fim]

    if pagina - 1 >= 1:
        anterior = f"pagina={pagina-1}&por_pagina{por_pagina}"
    if fim < len(dados):
        proxima = f"pagina={pagina+1}&por_pagina{por_pagina}"

    return  {
        "pagina": pagina,
        "anterior": anterior,
        "proxima": proxima,
        "dados": dados_pagina
    }
    