import json

class Tren:
    def __init__(self, id, velocidad, nombre, vagones):
        self.id = id
        self.velocidad = velocidad
        self.nombre = nombre
        self.vagones = vagones

    def capacidad_total(self):
        return sum(self.vagones)
    
    def __repr__(self):
        return f"Tren({self.nombre}, {self.velocidad} km/h, {self.capacidad_total()})"