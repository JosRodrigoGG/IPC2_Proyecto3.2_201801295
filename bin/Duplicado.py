class Duplicado():
    def __init__(self, referencia):
        self._referencia = referencia
        self._cantidad = 1

    def getReferencia(self):
        return self._referencia

    def getCantidad(self):
        return self._cantidad

    def setCantidad(self):
        self._cantidad += 1