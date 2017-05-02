import ArbolB, ArbolAvl

class NodoB(object):
	def __init__(self, nombre):
		self.nombre = nombre
		self.id = self.nombre.replace("(", "p_").replace(")", "_p").replace("-", "_g_").replace(" ", "_")
		if nombre == "/":
			self.id = "root"
		self.carpetas = None
		self.archivos = None

	def crearCarpeta(self, nombre):
		if self.carpetas == None:
			self.carpetas = ArbolB.ArbolB()
		self.carpetas.insertar(nombre)

	def eliminarCarpeta(self, nombre):
		if self.carpetas != None:
			self.carpetas.eliminar(nombre)

	def crearArchivo(self, nombre, contenido):
		if self.archivos == None:
			self.archivos = ArbolAvl.ArbolAvl()
		self.archivos.insertar(nombre, contenido)

	def eliminarArchivo(self, nombre):
		if self.archivos != None:
			self.archivos.eliminar(nombre)

	def renombrarArchivo(self, anterior, nuevo):
		if self.archivos != None:
			self.archivos.modificar(anterior, nuevo)