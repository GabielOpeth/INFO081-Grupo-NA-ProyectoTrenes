class Estacion:
    def __init__(self, id, nombre, poblacion, vias):
        self.id = id
        self.nombre = nombre
        self.poblacion = poblacion
        self.vias = vias
        
        self.andenes_ocupados = 0
        self.flujo_acumulado = 0
        self.pasajeros_esperando = 0

    def __repr__(self):
        return f"Estacion({self.nombre} | ID:{self.id})"

    def to_dict(self):
        return {
            "id": self.id, 
            "nombre": self.nombre, 
            "poblacion": self.poblacion, 
            "vias": self.vias,
            "flujo_acumulado": self.flujo_acumulado,
            "pasajeros_esperando": self.pasajeros_esperando
        }

class GestorEstaciones:
    def __init__(self):
        self.estaciones = {} 
        self.next_id = 1

    def crear(self, nombre, poblacion, vias):
        id_nuevo = self.next_id
        self.next_id += 1
        nueva_estacion = Estacion(id_nuevo, nombre, poblacion, vias)
        self.estaciones[id_nuevo] = nueva_estacion
        return nueva_estacion

    def consultar(self, id_estacion):
        return self.estaciones.get(id_estacion)
    
    def obtener_todas(self):
        return list(self.estaciones.values())