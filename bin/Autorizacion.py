from datetime import datetime

from bin.Aprobacion import Aprobacion
from bin.Errores import Errores
from lista.Lista import Lista


class Autorizacion():
    def __init__(self, facturas, facturasCorrectas, cantidadEmisores, cantidadReceptores):
        now = datetime.now()

        self._fecha = str(now.day) + '/' + str(now.month) + '/' + str(now.year)
        self._facturas = facturas
        self._listaErrores = Lista()
        self._totalErrores = 0
        self._facturasCorrectas = facturasCorrectas
        self._cantidadEmisores = cantidadEmisores
        self._cantidadReceptores = cantidadReceptores
        self._listaAprobacion = Lista()
        self._totalAprobacion = 0

    def agregarError(self, etiqueta, valor, referencia):
        self._listaErrores.agregar(Errores(etiqueta, valor, referencia))
        self._totalErrores = self._listaErrores.getCantidad()

    def agregarAprovacion(self, nit, referencia, codigo, fecha):
        self._listaAprobacion.agregar(Aprobacion(nit, referencia, codigo, fecha))
        self._totalAprobacion = self._listaAprobacion.getCantidad()

    def getFecha(self):
        return self._fecha

    def getFacturas(self):
        return self._facturas

    def getListaErrores(self):
        return self._listaErrores

    def getTotalErrores(self):
        return self._totalErrores

    def getFacturasCorrectas(self):
        return self._facturasCorrectas

    def getCantidadEmisores(self):
        return self._cantidadEmisores

    def cantidadReceptores(self):
        return self._cantidadReceptores

    def getListaAprobacion(self):
        return self._listaAprobacion

    def getTotalAprobacion(self):
        return self._totalAprobacion
