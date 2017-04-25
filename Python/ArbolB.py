import ArbolAvl, NodoAvl, NodoB, Pagina, subprocess

class ArbolB(object):
	def __init__ (self):
		self.raiz = Pagina.Pagina()
		self.orden = 5
		self.medio = self.orden / 2

	def __buscarNodo(self, actual, nombre, indice):
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
			esta, indice = self.__buscarNodo(actual, nombre, indice)
			if esta:
				return actual, indice
			else:
				return self.buscar(actual, nombre, indice)

	def crearCarpeta(self, nombre):
		nueva = NodoB.NodoB(nombre)
		self.raiz = self.__crearCarpeta(self.raiz, nueva)

	def __crearCarpeta(self, raiz, carpeta):
		subir = False
		mediana = NodoB.NodoB("")
		nueva = Pagina.Pagina()
		raiz_ = Pagina.Pagina()
		subir, mediana, nueva, raiz_ = self.__mover(raiz, carpeta, mediana, nueva)
		if subir:
			auxiliar = Pagina.Pagina()
			auxiliar.cuenta = 1
			auxiliar.nodos[1] = mediana
			auxiliar.ramas[0] = raiz_
			auxiliar.ramas[1] = nueva
			raiz_ = auxiliar
		return raiz_

	def __mover(self, actual, carpeta, mediana, nueva):
		subir = False
		if actual == None or actual.estaVacia():
			return True, carpeta, None, None
		else:
			indice = 0
			esta = False
			esta, indice = self.__buscarNodo(actual, carpeta.nombre, indice)
			if esta:
				print "Nombre de carpeta duplicada: '" + str(carpeta.nombre) + "'."
				return False, None, None, self.raiz
			subir, mediana, nueva, actual.ramas[indice] = self.__mover(actual.ramas[indice], carpeta, mediana, nueva)
			if subir:
				if actual.estaLlena():
					actual, mediana, nueva = self.__dividirPagina(actual, mediana, nueva, indice)
				else:
					actual = self.__insertarEnHoja(actual, mediana, nueva, indice)
					return False, None, None self.raiz
			return subir, mediana, nueva, actual

	def __dividirPagina(self, actual, mediana, nueva, indice):
		posicion = 0
		if (indice <= self.medio):
			posicion = self.medio
		else:
			posicion = self.medio + 1
		auxiliar = Pagina.Pagina()
		contador = posicion + 1
		while(contador < self.orden):
			auxiliar.nodos[contador - posicion] = actual.nodos[contador]
			auxiliar.ramas[contador - posicion] = actual.ramas[contador]
			contador = contador + 1
		auxiliar.cuenta = self.orden - (1 + posicion)
		actual.cuenta = posicion
		if (indice <= self.medio):
			actual = self.__insertarEnHoja(actual, mediana, nueva, indice)
		else:
			auxiliar = self.__insertarEnHoja(auxiliar, mediana, nueva, indice - posicion)
		auxiliar.ramas[0] = actual.ramas[actual.cuenta]
		actual.cuenta = actual.cuenta - 1
		return actual, actual.nodos[actual.cuenta], auxiliar

	def __insertarEnHoja(self, actual, nuevo, derecha, indice):
		posicion = actual.cuenta
		while (posicion >= indice + 1):
			actual.nodos[posicion + 1] = actual.nodos[posicion]
			actual.ramas[posicion + 1] = actual.ramas[posicion]
			posicion = posicion - 1
		actual.nodos[indice + 1] = nuevo
		actual.ramas[posicion + 1] = derecha
		actual.cuenta = actual.cuenta + 1
		return actual

	def eliminarCarpeta(self, nombre):
		self.raiz = self.__eliminarCarpeta(self.raiz, nombre)

	def __eliminarCarpeta(self, raiz, nombre):
		encontrado = False
		raiz_ = Pagina.Pagina()
		encontrado, raiz_ = self.__eliminarNodo(raiz, nombre, encontrado)
		if encontrado:
			print "Carpeta "+ ID + " fue eliminada."
			if raiz_.estaVacia():
				raiz_ = raiz_.ramas[0]
		else:
			print "No existe la carpeta."
			raiz_ = self.raiz
		return raiz_

	def __eliminarNodo(self, actual, nombre, encontrado):
		indice = 0
		if actual == None:
			return False, actual
		else:
			encontrado, indice = self.__buscarNodo(actual, nombre, indice)
			if encontrado:
				if actual.ramas[indice - 1] == None:
					actual = self.__remover(actual, indice)
				else:
					actual = self.__porSucesor(actual, indice)
					encontrado, actual.ramas[indice] = self.__eliminarNodo(actual.ramas[indice], actual.nodos[indice].nombre, encontrado)
			else:
				encontrado, actual.ramas[indice] = self.__eliminarNodo(actual.ramas[indice], nombre, encontrado)
			if actual.ramas[indice] != None and actual.ramas[indice].cuenta < self.medio:
				actual = self.__restaurar(actual, indice)
			return encontrado, actual

	def __remover(self, actual, indice):
		indice = indice + 1
		while (indice <= actual.cuenta):
			actual.nodos[indice - 1] = actual.nodos[indice]
			actual.ramas[indice - 1] = actual.ramas[indice]
			indice = indice + 1
		actual.cuenta = actual.cuenta - 1
		return actual

	def __porSucesor(self, actual, indice):
		auxiliar = actual.ramas[indice]
		while (auxiliar.ramas[0] != None):
			auxiliar = auxiliar.ramas[0]
		actual.nodos[indice] = auxiliar.nodos[1]
		return actual

	def __restaurar(self, actual, indice):
		if indice > 0:
			if actual.ramas[indice - 1].cuenta > self.medio:
				actual = self.__moverDerecha(actual, indice)
			else:
				self.__combinar(actual, indice)
		else:
			if actual.ramas[1].cuenta > self.medio:
				actual = self.__moverIzquierda(actual, 1)
			else:
				self.__combinar(actual, 1)
		return actual

	def __moverDerecha(self, actual, indice):
		problema = actual.ramas[indice]
		izquierda = actual.ramas[indice - 1]
		contador = problema.cuenta
		while(contador >= 1):
			problema.nodos[contador + 1] = problema.nodos[contador]
			problema.ramas[contador + 1] = problema.ramas[contador]
			contador = contador - 1
		problema.cuenta = problema.cuenta + 1
		problema.ramas[1] = problema.ramas[0]
		problema.nodos[1] = actual.nodos[indice]
		actual.nodos[indice] = izquierda.nodos[izquierda.cuenta]
		problema.ramas[0] = izquierda.ramas[izquierda.cuenta]
		izquierda.cuenta = izquierda.cuenta - 1
		return actual

	def __moverIzquierda(self, actual, indice):
		problema = actual.ramas[indice - 1]
		derecha = actual.ramas[indice]
		problema.cuenta = problema.cuenta + 1
		problema.nodos[problema.cuenta] = actual.nodos[indice]
		problema.ramas[problema.cuenta] = derecha.ramas[0]
		actual.nodos[indice] = derecha.nodos[1]
		derecha.ramas[1] = derecha.ramas[0]
		derecha.cuenta = derecha.cuenta - 1
		contador = 1
		while (contador <= derecha.cuenta):
			derecha.nodos[contador] = derecha.nodos[contador + 1]
			derecha.ramas[contador] = derecha.ramas[contador + 1]
			contador = contador + 1
		return actual

	def __combinar(self, padre, indice):
		auxiliar = padre.ramas[indice]
		izquierdo = padre.ramas[indice - 1]
		izquierdo.cuenta = izquierdo.cuenta - 1
		izquierdo.nodos[izquierdo.cuenta] = padre.nodos[indice]
		izquierdo.ramas[izquierdo.cuenta] = auxiliar.ramas[0]
		contador = 1
		while(contador <= auxiliar.cuenta):
			izquierdo.cuenta = izquierdo.cuenta + 1
			izquierdo.nodos[izquierdo.cuenta] = auxiliar.nodos[contador]
			izquierdo.ramas[izquierdo.cuenta] = auxiliar.ramas[contador]
			contador = contador + 1
		contador = indice
		while(contador <= padre.cuenta):
			padre.nodos[contador] = padre.nodos[contador + 1]
			padre.ramas[contador] = padre.ramas[contador + 1]
			contador = contador + 1
		padre.cuenta = padre.cuenta - 1

	def graficar(self):
		if self.raiz == None or self.raiz.estaVacia():
			return
		grafo = "digraph ArbolB{\n\trankdir = UD;\n\tgraph [ratio = fill];\n\tnode [shape = plaintext]\n\t"
		grafo = self.__enlistar(self.raiz, grafo) + "\n\n\t"
		grafo = self.__enlazar(self.raiz, grafo) + "\n}"
		Archivo = open('/home/moramaz/Escritorio/ArbolB.dot', 'w')
		Archivo.write(grafo)
		Archivo.close()
		subprocess.call(['dot', '/home/moramaz/Escritorio/ArbolB.dot', '-o', '/home/moramaz/Escritorio/ArbolB.png', '-Tpng', '-Gcharset=utf8']) 

	def __enlistar(self, raiz, grafo):
		if raiz == None or raiz.estaVacia():
			return grafo
		grafo = grafo + "N" + raiz.nodos[1].nombre + " [label=<\n\t\t<TABLE ALIGN = \"LEFT\">\n\t\t\t<TR>\n"
		contador = 1
		while(contador < self.orden):
			if contador <= raiz.cuenta:
				grafo = grafo + "\t\t\t\t<TD> " + raiz.nodos[contador].nombre + " \t\t\t\t</TD>\n"
			else:
				grafo = grafo + "\t\t\t\t<TD>  \t\t\t\t</TD>\n"
		grafo = grafo + "\t\t\t</TR>\n\t\t</TABLE>\n\t>, ];\n\t"
		for i in raiz.ramas:
			grafo = self.__enlistar(i, grafo)
		return grafo

	def __enlazar(self, raiz, grafo):
		if raiz == None or raiz.estaVacia():
			return grafo
		for i in raiz.ramas:
			grafo = self.enlazar(i, grafo)
			if i != None:
				grafo = grafo + "N" + raiz.nodos[1].nombre + " -> N" + i.nodos[1].nombre + ";\n\t"
		return grafo
