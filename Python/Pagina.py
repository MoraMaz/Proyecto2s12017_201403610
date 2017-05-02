class Pagina(object):
	def __init__(self):
		self.nodos = [None, None, None, None, None]
		self.ramas = [None, None, None, None, None]
		self.cuenta = 0

	def estaLlena(self):
		return (self.cuenta == 4)

	def estaVacia(self):
		return (self.cuenta == 0)