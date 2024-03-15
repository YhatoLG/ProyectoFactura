from modelo.Persona import Persona
class Cliente(Persona):
    def __init__(self,credito=None):
        self.credito=credito

    def setcredito(self,credito=None):
        self.credito=credito
    def getCredito(self):
        return self.credito
