import json

class Estacion:
    def _init_(self, id, nombre, poblacion, vias):
        self.id = id
        self.nombre = nombre
        self.poblacion = poblacion
        self.vias = vias

    def _repr_(self):
        return f"Estacion({self.nombre}, Poblacion: {self.poblacion})"
