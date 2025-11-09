import json

class Estacion:
    def __init__(self, id, nombre, poblacion, vias):
        self.id = id
        self.nombre = nombre
        self.poblacion = poblacion
        self.vias = vias

    def __repr__(self):
        return f"Estacion({self.nombre}, Poblacion: {self.poblacion})"
