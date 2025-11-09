import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class Estacion:
    def __init__(self, id, nombre, poblacion, vias):
        self.id = id
        self.nombre = nombre
        self.poblacion = poblacion
        self.vias = vias

    def __repr__(self):
        return f"Estacion({self.nombre}, Poblacion: {self.poblacion})"
    

class Ruta:
    def __init__(self, origen, destino, longitud_km):
        self.origen = origen
        self.destino = destino
        self.longitud_km = longitud_km

    def __repr__(self):
        return "Ruta({self.origen}, {self.destino}, {self.longitud_km} km)"

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