import json

class Estacion:
    def __init__(self, id, nombre, poblacion, vias):
        self.id = id
        self.nombre = nombre
        self.poblacion = poblacion
        self.vias = vias

    def __repr__(self):
        return f"Estacion(ID: {self.id}, Nombre: {self.nombre}, Vias: {self.vias})"

    def dick(self):
        return {"id": self.id, "nombre": self.nombre, "poblacion": self.poblacion, "vias": self.vias}

class GestorEstaciones:
    def __init__(self):
        self.estaciones = {} 
        self.next_id = 1

    def _obtener_id(self):
        id_gen = self.next_id
        self.next_id += 1
        return id_gen

    def crear(self, nombre, poblacion, vias):
        id_nuevo = self._obtener_id()
        nueva_estacion = Estacion(id_nuevo, nombre, poblacion, vias)
        self.estaciones[id_nuevo] = nueva_estacion
        return nueva_estacion

    def modificar(self, id_estacion, nombre=None, poblacion=None, vias=None):
        if id_estacion not in self.estaciones:
            return False, "Estación no encontrada."
        
        estacion = self.estaciones[id_estacion]
        
        if nombre is not None:
            estacion.nombre = nombre
        elif poblacion is not None:
            estacion.poblacion = poblacion
        elif vias is not None:
            estacion.vias = vias
            
        return True, estacion
    
    def eliminar(self, id_estacion):
        if id_estacion in self.estaciones:
            del self.estaciones[id_estacion]
            return True, "Estación eliminada."
        return False, "Estación no encontrada."

    def consultar(self, id_estacion):
        return self.estaciones.get(id_estacion)
