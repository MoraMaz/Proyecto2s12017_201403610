import NodoAvl
import subprocess

class Avl(object):
	def __init__(self):
		self.raiz = None
		self.altura = -1
		self.equilibrio = 0

	def insertar(self, nombre, archivo):
		nuevo = NodoAvl.NodoAvl(nombre, archivo)
		if self.raiz == None:
			self.raiz = nuevo
			self.raiz.derecho = Avl()
			self.raiz.izquierdo = Avl()
		elif self.raiz.nombre < nombre:
			self.raiz.derecho.insertar(nombre, archivo)
		elif self.raiz.nombre > nombre:
			self.raiz.izquierdo.insertar(nombre, archivo)
		else:
			print "El archivo ya existe."
		self.balancear()

	def balancear(self):
		self.actualizarAlturas(recursivo = False)
		self.actualizarEquilibrio(False)
		while self.equilibrio < -1 or self.equilibrio > 1:
			if self.equilibrio > 1:
				if self.raiz.izquierdo.equilibrio < 0:
					self.raiz.izquierdo.rotacionIzquierda()
					self.actualizarAlturas()
					self.actualizarEquilibrio()
				raiz = self.raiz
				self.raiz = raiz.izquierdo.raiz
				raiz.izquierdo.raiz = self.raiz.derecho.raiz
				self.raiz.derecho.raiz = raiz
				self.actualizarAlturas()
				self.actualizarEquilibrio()
			if self.equilibrio < -1:
				if self.raiz.derecho.equilibrio > 0:
					self.raiz.derecho.rotacionDerecha()
					self.actualizarAlturas()
					self.actualizarEquilibrio()
				raiz = self.raiz
				self.raiz = raiz.derecho.raiz
				raiz.derecho.raiz = self.raiz.izquierdo.raiz
				self.raiz.izquierdo.raiz = raiz
				self.actualizarAlturas()
				self.actualizarEquilibrio()

	def actualizarAlturas(self, recursivo = True):
		if self.raiz == None:
			self.altura = -1
		else:
			if recursivo:
				if self.raiz.izquierdo != None:
					self.raiz.izquierdo.actualizarAlturas()
				if self.raiz.derecho != None:
					self.raiz.derecho.actualizarAlturas()
			self.altura = max(self.raiz.izquierdo.altura, self.raiz.derecho.altura) + 1

	def actualizarEquilibrio(self, recursivo = True):
		if self.raiz == None:
			self.equilibrio = 0
		else:
			if recursivo:
				if self.raiz.izquierdo != None:
					self.raiz.izquierdo.actualizarEquilibrio()
				if self.raiz.derecho != None:
					self.raiz.derecho.actualizarEquilibrio()
			self.equilibrio = self.raiz.izquierdo.altura - self.raiz.derecho.altura

	def rotacionDerecha(self):
		raiz = self.raiz
		self.raiz = raiz.izquierdo.raiz
		raiz.izquierdo.raiz = self.raiz.derecho.raiz
		self.raiz.derecho.raiz = raiz

	def rotacionIzquierda(self):
		raiz = self.raiz
		self.raiz = raiz.derecho.raiz
		raiz.derecho.raiz = self.raiz.izquierdo.raiz
		self.raiz.izquierdo.raiz = raiz

	def eliminar(self, nombre):
		if self.raiz != None:
			if self.raiz.nombre == nombre:
				if self.raiz.izquierdo.raiz == None and self.raiz.derecho.raiz == None:
					self.raiz = None
				elif self.raiz.izquierdo.raiz != None and self.raiz.derecho.raiz == None:
					self.raiz = self.raiz.izquierdo.raiz
				elif self.raiz.izquierdo.raiz == None and self.raiz.derecho.raiz != None:
					self.raiz = self.raiz.derecho.raiz
				else:
					predecesor = self.raiz.izquierdo.raiz
					while predecesor.derecho.raiz != None:
						predecesor = predecesor.derecho.raiz
					if predecesor != None:
						self.raiz.nombre = predecesor.nombre
						self.raiz.archivo = predecesor.archivo
						self.raiz.izquierdo.eliminar(predecesor.nombre)
			elif self.raiz.nombre < nombre:
				self.raiz.derecho.eliminar(nombre)
			elif self.raiz.nombre > nombre:
				self.raiz.izquierdo.eliminar(nombre)
			self.balancear()

	def obtenerContenido(self, nombre):
		if self.raiz.nombre == nombre:
			return self.raiz.archivo
		elif self.raiz.nombre < nombre:
			return self.raiz.derecho.obtenerContenido(nombre)
		elif self.raiz.nombre > nombre:
			return self.raiz.izquierdo.obtenerContenido(nombre)

	def modificar(self, anterior, nuevo):
		contenido = self.obtenerContenido(anterior)
		self.eliminar(anterior)
		self.insertar(nuevo, contenido)

	def graficar(self):
		cadena = "digraph arbol {\n"
		if(self.raiz != None):
			cadena = self.__listar(self.raiz, cadena)
			cadena += "\n"
			cadena = self.__enlazar(self.raiz, cadena)
		cadena += "}"
		Archivo = open('/home/moramaz/Escritorio/Avl.dot', 'w')
		Archivo.write(cadena)
		Archivo.close()
		subprocess.call(['dot', '/home/moramaz/Escritorio/Avl.dot', '-o', '/home/moramaz/Escritorio/Avl.png', '-Tpng', '-Gcharset=utf8']) 

	def __listar(self, raiz, cadena):
		if(raiz != None):
			cadena += "n" + str("".join(raiz.nombre.split("."))) + " [label = \"" + str(raiz.nombre) + "\"];\n"
#			cadena += "n" + str("".join(raiz.nombre.split("."))) + " [label = \"" + str(raiz.nombre) + "\n" + str(raiz.archivo) + "\"];\n" # para que en el nodo salga la informacion del archivo
			if(raiz.izquierdo != None and raiz.derecho != None):
				cadena = self.__listar(raiz.izquierdo.raiz, cadena)
				cadena = self.__listar(raiz.derecho.raiz, cadena)
			elif(raiz.raiz.izquierdo != None):
				cadena = self.__listar(raiz.izquierdo.raiz, cadena)
			elif(raiz.raiz.derecho != None):
				cadena = self.__listar(raiz.derecho.raiz, cadena)
		return cadena;

	def __enlazar(self, raiz, cadena):
		if(raiz != None):
			if(raiz.derecho.raiz != None):
				cadena += "n" + str("".join(raiz.nombre.split("."))) + " -> n" + str("".join(raiz.derecho.raiz.nombre.split("."))) + ";\n"
				cadena = self.__enlazar(raiz.derecho.raiz, cadena)
			if(raiz.izquierdo.raiz != None):
				cadena += "n" + str("".join(raiz.nombre.split("."))) + " -> n" + str("".join(raiz.izquierdo.raiz.nombre.split("."))) + ";\n"
				cadena = self.__enlazar(raiz.izquierdo.raiz, cadena)
		return cadena

tree = Avl()
# descomentando uno a uno se ve el proceso
tree.insertar("hola.jpg", "hola1")
#tree.insertar("hola.png", "hola2")
#tree.insertar("hola.txt", "hola3")
#tree.insertar("hola.zip", "hola4")
#tree.insertar("hola.wma", "hola5")
#tree.insertar("hola.mp3", "hola6")
#tree.insertar("hola.mp4", "hola7")
#tree.modificar("hola.png", "imagen.png")
#tree.modificar("hola.mp4", "video.mp4")
#tree.modificar("hola.wma", "video.wma")
#tree.modificar("hola.txt", "texto.txt")
#tree.modificar("hola.mp3", "camcion.mp3")
#tree.modificar("camcion.mp3", "cancion.mp3")
#tree.modificar("hola.jpg", "imagen.jpg")
#tree.modificar("hola.zip", "comprimido.zip")
tree.graficar()