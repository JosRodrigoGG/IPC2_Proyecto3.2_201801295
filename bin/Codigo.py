class Codigo():
    def __init__(self):
        self._codigo = 201801295000

    def getCodigo(self):
        return self._codigo

    def uso(self):
        self._codigo += 1

    def reinicar(self):
        self._codigo = 201801295000