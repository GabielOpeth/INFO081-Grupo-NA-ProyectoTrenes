class Tren:
    def __init__(self, id, velocidad, nombre, vagones):
        self.id = id
        self.velocidad = velocidad
        self.nombre = nombre
        self.vagones = vagones

    def capacidad_total(self):
        if isinstance(self.vagones, list):
            return sum(self.vagones)
        return self.vagones
    
    def __repr__(self):
        return f"Tren(ID: {self.id}, {self.nombre}, {self.velocidad} km/h, Capacidad: {self.capacidad_total()})"

    def dick(self):
        return {"id": self.id, "velocidad": self.velocidad, "nombre": self.nombre, "vagones": self.vagones}

class GestorTrenes:
    def __init__(self):
        self.trenes = {}      
        self.next_id = 1

    def _obtener_id(self):
        id_gen = self.next_id
        self.next_id += 1
        return id_gen

    def crear(self, velocidad, nombre, vagones):
        id_nuevo = self._obtener_id()
        nuevo_tren = Tren(id_nuevo, velocidad, nombre, vagones)
        self.trenes[id_nuevo] = nuevo_tren
        return nuevo_tren

    def modificar(self, id_tren, velocidad=None, nombre=None, vagones=None):
        if id_tren not in self.trenes:
            return False, "Tren no encontrado."
        
        tren = self.trenes[id_tren]
        
        if velocidad is not None:
            tren.velocidad = velocidad
        elif nombre is not None:
            tren.nombre = nombre
        elif vagones is not None:
            tren.vagones = vagones
            
        return True, tren
    
    def eliminar(self, id_tren):
        if id_tren in self.trenes:
            del self.trenes[id_tren]
            return True, "Tren eliminado."
        return False, "Tren no encontrado."

    def consultar(self, id_tren):
        return self.trenes.get(id_tren)
