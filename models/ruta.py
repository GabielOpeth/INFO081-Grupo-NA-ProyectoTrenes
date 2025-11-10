import json

class Ruta:
    def __init__(self, origen, destino, longitud_km):
        self.origen = origen
        self.destino = destino
        self.longitud_km = longitud_km

    def __repr__(self):
        return "Ruta({self.origen}, {self.destino}, {self.longitud_km} km)"