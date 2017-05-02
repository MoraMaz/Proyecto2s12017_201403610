import NodoDoble

class ListaDoble(object):
	def __init__(self):
		self.inicio = None

	def insertar(self, nombre, contrasenha):
		if self.inicio == None:
			self.inicio = NodoDoble.NodoDoble(nombre, contrasenha)
		else:
			if not self.__existe(nombre):
				nuevo = NodoDoble.NodoDoble(nombre, contrasenha)
				auxiliar = self.inicio
				while(auxiliar.siguiente != None):
					auxiliar = auxiliar.siguiente
				nuevo.anterior = auxiliar
				auxiliar.siguiente = nuevo

	def __existe(self, nombre):
		auxiliar = self.inicio
		while(auxiliar != None):
			if auxiliar.nombre = nombre:
				return True
			auxiliar = auxiliar.siguiente
		return False