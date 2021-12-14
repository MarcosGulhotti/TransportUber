class CpfFormatError(Exception):
  ...

class CelularFormatError(Exception):
  ...

class RequiredKeysError(Exception):
  ...

class LoginKeysError(Exception):
  ...

class CategoryTypeError(Exception):
    tipos = {
        str: "string",
        int: "integer",
        float: "float",
        list: "list",
        dict: "dictionary",
        bool: "boolean",
    }

    def __init__(self, categoria, volume):
        self.message = {"erro de tipagem ": [
            {"categoria": f'{self.tipos[type(categoria)]}, deve ser tipo dictionary list.'},
            {"volume": f'{self.tipos[type(volume)]}, deve ser tipo float.'},
        ]}
        super().__init__(self.message)

class PrevisaoEntregaFormatError(Exception):
  ...

class PlacaFormatError(Exception):
  ...

class NotaInvalidaError(Exception):
  ...

class EntregaNãoEstaEmMovimentoError(Exception):
  ...