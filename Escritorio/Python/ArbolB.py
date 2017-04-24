import ArbolAvl, NodoAvl, NodoB, Pagina

class ArbolB(object):
	def __init__ (self):
		self.raiz = Pagina.Pagina()
		self.orden = 5

	def buscarNodo(self, actual, nombre, indice):
		if nombre < actual.nodos[1].nombre:
			return False, 0
		else:
			indice = actual.cuenta
			while (nombre < actual.nodos[indice].nombre and indice > 1):
				indice = indice - 1
			return nombre == actual.nodos[indice].nombre, indice

	def buscar(self, actual, nombre, indice):
		if actual == None:
			return actual, indice
		else:
			esta = False
			esta, indice = self.buscarNodo(actual, nombre, indice)
			if esta:
				return actual, indice
			else:
				return self.buscar(actual, nombre, indice)

	def crearCarpeta(self, nombre):
		nueva = NodoB.NodoB(nombre)
		self.raiz = self.crearCarpeta(self.raiz, nueva)

	def crearCarpeta(self, raiz, carpeta):
		subir = False
		mediana = NodoB.NodoB("")
		nueva = Pagina.Pagina()
		raiz_ = Pagina.Pagina()
		subir, mediana, nueva, raiz_ = self.mover(raiz, carpeta, mediana, nueva)
		if subir:
			auxiliar = Pagina.Pagina()
			auxiliar.cuenta = 1
			auxiliar.nodos[1] = mediana
			auxiliar.ramas[0] = raiz_
			auxiliar.ramas[1] = nueva
			raiz_ = auxiliar
		return raiz_

	def mover(self, actual, carpeta, mediana, nueva):
		subir = False
		if actual == None or actual.estaVacia():
			return True, carpeta, None, None
		else:
			indice = 0
			esta = False
			esta, indice = self.buscarNodo(actual, carpeta.nombre, indice)
			if esta:
				print "Carpeta duplicada: '" + str(carpeta.nombre) + "'."
				return False, None, None, self.raiz
			subir, mediana, nueva, actual.ramas[indice] = self.mover(actual.ramas[indice], carpeta, mediana, nueva)
			if subir:
				if actual.estaLlena():
					actual, mediana, nueva = self.dividirPagina(actual, mediana, nueva, indice)
				else:
					self.insertarEnHoja(actual, mediana, nueva, indice)
					return False, None, None self.raiz
			return subir, mediana, nueva, actual

	def dividirPagina(self, actual, mediana, nueva, indice):
		posicion = 0
		if (Indice <= self.orden / 2):
			posicion = self.orden / 2
		else:
			posicion = (self.orden / 2) + 1
		auxiliar = Pagina.Pagina()
		contador = posicion + 1
		while(contador < self.orden):
			auxiliar.nodos[contador - posicion] = actual.nodos[contador]
			auxiliar.ramas[contador - posicion] = actual.ramas[contador]
			contador = contador + 1
		auxiliar.cuenta = self.orden - 1 - posicion
		actual.cuenta = posicion
		if (Indice <= self.orden / 2):
			self.insertarEnHoja(actual, mediana, nueva, indice)
		else:
			self.insertarEnHoja(actual, mediana, nueva, indice - posicion)
		auxiliar.ramas[0] = actual.ramas[actual.cuenta]
		actual.cuenta = actual.cuenta - 1
		return actual, actual.nodos[actual.cuenta], auxiliar