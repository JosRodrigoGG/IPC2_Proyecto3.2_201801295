class Nodo():
    def __init__(self, dato):
        self.anterior = None
        self.dato = dato
        self.siguiente = None

    def setAnterior(self, anterior):
        self.anterior = anterior

    def setDato(self, dato):
        self.dato = dato

    def setSiguiente(self, siguiente):
        self.siguiente = siguiente

    def getAnterior(self):
        return self.anterior

    def getDato(self):
        return self.dato

    def getSiguiente(self):
        return self.siguiente
