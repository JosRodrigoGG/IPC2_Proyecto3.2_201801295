class Errores():
    def __init__(self, etiqueta, valor, referencia):
        self._etiqueta = etiqueta
        self._valor = valor
        self._referencia = referencia

    def getEtiqueta(self):
        return self._etiqueta

    def getValor(self):
        return self._valor

    def getReferencia(self):
        return self._referencia
