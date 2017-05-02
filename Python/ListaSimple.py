import NodoSimple

class ListaSimple(object):
	def __init__(self):
		self.inicio = None

	def insertar(self, informacion):
		if self.inicio == None:
			self.inicio = NodoSimple.NodoSimple(informacion)
		else:
			auxiliar = self.inicio
			while(auxiliar.siguiente != None):
				auxiliar = auxiliar.siguiente
			auxiliar.siguiente = NodoSimple.NodoSimple(informacion)