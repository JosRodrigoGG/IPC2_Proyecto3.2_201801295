from bin.Fecha import Fecha


class DTE():
    def __init__(self, tiempo, referencia, nitEmisor, nitReseptor, valor, iva, total):
        self._tiempo = tiempo
        self._fecha = None
        self._referencia = referencia
        self._nitEmisor = nitEmisor
        self._nitReseptor = nitReseptor
        self._valor = valor
        self._iva = iva
        self._total = total

    def crearFecha(self, dia, hora):
        self._fecha = Fecha(dia, hora)

    def getTiempo(self):
        return self._tiempo

    def getFecha(self):
        return self._fecha

    def getReferencia(self):
        return self._referencia

    def getNitEmisor(self):
        return self._nitEmisor

    def getNitReseptor(self):
        return self._nitReseptor

    def getValor(self):
        return self._valor

    def getIva(self):
        return self._iva

    def getTotal(self):
        return self._total