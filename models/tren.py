#Clase del modelo en concrteo
class Tren:
    def __init__(self, id, velocidad, nombre, vagones):
        self.id = id
        self.velocidad = velocidad
        self.nombre = nombre
        self.vagones = vagones
        
        self.ubicacion_actual = None
        self.ruta_actual = None
        self.distancia_recorrida_ruta = 0

    def capacidad_total(self):
        if isinstance(self.vagones, list):
            return sum(self.vagones)
        if isinstance(self.vagones, int):
             return self.vagones * 50
        return 0
    
    def __repr__(self):
        return f"Tren({self.nombre} | Vel:{self.velocidad})"

    def to_dict(self):
        ub_data = "En ruta"
        if hasattr(self.ubicacion_actual, 'id'):
            ub_data = self.ubicacion_actual.id
        elif self.ubicacion_actual:
             ub_data = str(self.ubicacion_actual)

        return {
            "id": self.id, 
            "velocidad": self.velocidad, 
            "nombre": self.nombre, 
            "vagones": self.vagones,
            "ubicacion_actual": ub_data,
            "distancia_recorrida": self.distancia_recorrida_ruta
        }
#Gestor de la clase en si
class GestorTrenes:
    def __init__(self):
        self.trenes = {}      
        self.next_id = 1

    def crear(self, velocidad, nombre, vagones):
        id_nuevo = self.next_id
        self.next_id += 1
        nuevo_tren = Tren(id_nuevo, velocidad, nombre, vagones)
        self.trenes[id_nuevo] = nuevo_tren
        return nuevo_tren

    def consultar(self, id_tren):
        return self.trenes.get(id_tren)

    def obtener_todos(self):
        return list(self.trenes.values())

    def modificar(self, id_tren, velocidad=None, nombre=None, vagones=None):
        if id_tren not in self.trenes:
            return False, "Tren no encontrado."
        
        tren = self.trenes[id_tren]
        if velocidad: tren.velocidad = velocidad
        if nombre: tren.nombre = nombre
        if vagones: tren.vagones = vagones
        return True, "Tren modificado."

    def eliminar(self, id_tren):
        if id_tren in self.trenes:
            del self.trenes[id_tren]
            return True, "Tren eliminado."
        return False, "Tren no encontrado."