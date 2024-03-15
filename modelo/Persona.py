class Persona(object):
    def __init__(self,codigo=None,nombre=None,telefono=None,email=None):
        self.codigo=codigo
        self.nombre=nombre
        self.telefono=telefono
        self.email=email
    def setCodigo(self,codigo=None):
        self.codigo=codigo
    def getCodigo(self):
        return self.codigo

    def setNombre(self,nombre=None):
        self.nombre=nombre
    def getNombre(self):
        return self.nombre

    def setTelefono(self,telefono=None):
        self.telefono=telefono
    def getTelefono(self):
        return self.telefono
    
    def setEmail(self,email=None):
        self.email=email
    def getEmail(self):
        return self.email