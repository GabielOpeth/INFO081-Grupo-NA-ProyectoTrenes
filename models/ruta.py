#Clase del modelo en concreto
class Ruta:
    def __init__(self, id, origen, destino, longitud_km):
        self.id = id
        self.origen = origen
        self.destino = destino
        self.longitud_km = longitud_km

    def __repr__(self):
        nom_origen = self.origen.nombre if hasattr(self.origen, 'nombre') else self.origen
        nom_destino = self.destino.nombre if hasattr(self.destino, 'nombre') else self.destino
        return f"Ruta({nom_origen} -> {nom_destino})"

    def to_dict(self):
        origen_id = self.origen.id if hasattr(self.origen, 'id') else str(self.origen)
        destino_id = self.destino.id if hasattr(self.destino, 'id') else str(self.destino)
        return {
            "id": self.id, 
            "origen_id": origen_id, 
            "destino_id": destino_id, 
            "longitud_km": self.longitud_km
        }
#Gestor de la clase en si
class GestorRutas:
    def __init__(self):
        self.rutas = {}      
        self.next_id = 1

    def crear(self, origen, destino, longitud_km):
        id_nuevo = self.next_id
        self.next_id += 1
        nueva_ruta = Ruta(id_nuevo, origen, destino, longitud_km) 
        self.rutas[id_nuevo] = nueva_ruta
        return nueva_ruta

    def consultar(self, id_ruta):
        return self.rutas.get(id_ruta)
        
    def obtener_todas(self):
        return list(self.rutas.values())

    def modificar(self, id_ruta, longitud_km=None):
        if id_ruta not in self.rutas:
            return False, "Ruta no encontrada"
        
        ruta = self.rutas[id_ruta]
        if longitud_km: ruta.longitud_km = longitud_km
        return True, "Ruta modificada"

    def eliminar(self, id_ruta):
        if id_ruta in self.rutas:
            del self.rutas[id_ruta]
            return True, "Ruta eliminada"
        return False, "Ruta no encontrada"