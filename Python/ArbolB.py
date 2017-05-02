import NodoB, Pagina, subprocess

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

	def insertar(self, nombre):
		nueva = NodoB.NodoB(nombre)
		self.raiz = self.__insertar(self.raiz, nueva)

	def __insertar(self, raiz, carpeta):
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
					return False, mediana, nueva, actual
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
		auxiliar.cuenta = (self.orden - 1) - posicion
		actual.cuenta = posicion
		if (indice <= self.medio):
			actual = self.__insertarEnHoja(actual, mediana, nueva, indice)
		else:
			auxiliar = self.__insertarEnHoja(auxiliar, mediana, nueva, indice - posicion)
		mediana = actual.nodos[actual.cuenta]
		auxiliar.ramas[0] = actual.ramas[actual.cuenta]
		actual.cuenta = actual.cuenta - 1
		return actual, mediana, auxiliar

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

	def eliminar(self, nombre):
		self.raiz = self.__eliminar(self.raiz, nombre)

	def __eliminar(self, raiz, nombre):
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

	def modificar(self, anterior, actual):
		#falta pensarlo :'v

	def graficar(self):
		if self.raiz != None or not self.raiz.estaVacia():
			cadena = "digraph ArbolB{\n\trankdir = UD;\n\tgraph [ratio = fill];\n\tnode [shape = plaintext]\n\t"
			cadena = self.__enlistar(self.raiz, cadena)
			cadena = cadena + "\n\n\t"
			cadena = self.__enlazar(self.raiz, cadena)
			cadena = cadena + "\n}"
			Archivo = open('/home/moramaz/Escritorio/ArbolB.dot', 'w')
			Archivo.write(cadena)
			Archivo.close()
			subprocess.call(['dot', '/home/moramaz/Escritorio/ArbolB.dot', '-o', '/home/moramaz/Escritorio/ArbolB.png', '-Tpng', '-Gcharset=utf8']) 

	def __enlistar(self, raiz, cadena):
		if raiz == None or raiz.estaVacia():
			return cadena
		cadena = cadena + "N" + raiz.nodos[1].id + " [label=<\n\t\t<TABLE ALIGN = \"LEFT\">\n\t\t\t<TR>\n"
		contador = 1
		while(contador < self.orden):
			if contador <= raiz.cuenta:
				cadena = cadena + "\t\t\t\t<TD> " + raiz.nodos[contador].nombre + " \t\t\t\t</TD>\n"
			else:
				cadena = cadena + "\t\t\t\t<TD>  \t\t\t\t</TD>\n"
			contador = contador + 1
		cadena = cadena + "\t\t\t</TR>\n\t\t</TABLE>\n\t>, ];\n\t"
		auxiliar = raiz.ramas[0]
		while(auxiliar != None):
			if auxiliar == raiz.ramas[0]:
				cadena = self.__enlistar(auxiliar, cadena)
				auxiliar = raiz.ramas[1]
			elif auxiliar == raiz.ramas[1]:
				cadena = self.__enlistar(auxiliar, cadena)
				auxiliar = raiz.ramas[2]
			elif auxiliar == raiz.ramas[2]:
				cadena = self.__enlistar(auxiliar, cadena)
				auxiliar = raiz.ramas[3]
			elif auxiliar == raiz.ramas[3]:
				cadena = self.__enlistar(auxiliar, cadena)
				auxiliar = raiz.ramas[4]
			elif auxiliar == raiz.ramas[4]:
				cadena = self.__enlistar(auxiliar, cadena)
				break
		return cadena

	def __enlazar(self, raiz, cadena):
		if raiz == None or raiz.estaVacia():
			return cadena
		auxiliar = raiz.ramas[0]
		while(auxiliar != None):
			if auxiliar == raiz.ramas[0]:
				cadena = self.__enlazar(auxiliar, cadena)
				if auxiliar != None:
					cadena = cadena + "N" + raiz.nodos[1].id + " -> N" + auxiliar.nodos[1].id + ";\n\t"
				auxiliar = raiz.ramas[1]
			elif auxiliar == raiz.ramas[1]:
				cadena = self.__enlazar(auxiliar, cadena)
				if auxiliar != None:
					cadena = cadena + "N" + raiz.nodos[1].id + " -> N" + auxiliar.nodos[1].id + ";\n\t"
				auxiliar = raiz.ramas[2]
			elif auxiliar == raiz.ramas[2]:
				cadena = self.__enlazar(auxiliar, cadena)
				if auxiliar != None:
					cadena = cadena + "N" + raiz.nodos[1].id + " -> N" + auxiliar.nodos[1].id + ";\n\t"
				auxiliar = raiz.ramas[3]
			elif auxiliar == raiz.ramas[3]:
				cadena = self.__enlazar(auxiliar, cadena)
				if auxiliar != None:
					cadena = cadena + "N" + raiz.nodos[1].id + " -> N" + auxiliar.nodos[1].id + ";\n\t"
				auxiliar = raiz.ramas[4]
			elif auxiliar == raiz.ramas[4]:
				cadena = self.__enlazar(auxiliar, cadena)
				if auxiliar != None:
					cadena = cadena + "N" + raiz.nodos[1].id + " -> N" + auxiliar.nodos[1].id + ";\n\t"
					break
		return cadena

Arbol = ArbolB()
# aca tambien, descomentando uno a uno se ve el proceso
#Arbol.insertar("nueva carpeta")
#Arbol.insertar("nueva carpeta 1")
#Arbol.insertar("nueva carpeta 2")
#Arbol.insertar("carpeta")
#Arbol.insertar("carpeta nueva")
#Arbol.insertar("carpeta nueva 2")
#Arbol.insertar("carpeta nueva (2)")
#Arbol.insertar("carpeta nueva (2) - copia")
Arbol.graficar()