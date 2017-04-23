class NodoAvl(object):
	def __init__(self, nombre, archivo):
		self.nombre = nombre
		self.archivo = archivo
		self.izquierdo = None
		self.derecho = None