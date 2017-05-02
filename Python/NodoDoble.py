import NodoB

class NodoDoble(object):
	def __init__(self, nombre, contrasenha):
		self.nombre = nombre
		self.contrasenha = contrasenha
		self.root = NodoB.NodoB("/")
		self.siguiente = None
		self.anterior = None