class Aprobacion:
    def __init__(self, nit, referencia, codigo, fecha):
        self._nit = nit
        self._referencia = referencia
        self._codigo = codigo
        self._fecha = fecha

    def getNit(self):
        return self._nit

    def getReferencia(self):
        return self._referencia

    def getCodigo(self):
        return self._codigo

    def getFecha(self):
        return self._fecha
