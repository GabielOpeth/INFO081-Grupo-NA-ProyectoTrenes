#El siguiente archivo es respecto al modelo Ruta: ruta.py

class Ruta:
    def __init__(self, id, origen, destino, longitud_km):
        self.id = id
        self.origen = origen
        self.destino = destino
        self.longitud_km = longitud_km

    def __repr__(self):
        return f"Ruta(ID: {self.id}, {self.origen} -> {self.destino}, {self.longitud_km} km)"

    def to_dict(self):
        return {"id": self.id, "origen": self.origen, "destino": self.destino, "longitud_km": self.longitud_km}

#Seccion de la gestion del modelo.

class GestorRutas:
    def __init__(self):
        self.rutas = {}      
        self.next_id = 1

    def _obtener_id(self):
        id_gen = self.next_id
        self.next_id += 1
        return id_gen

    def crear(self, origen, destino, longitud_km):
        id_nuevo = self._obtener_id()
        nueva_ruta = Ruta(id_nuevo, origen, destino, longitud_km) 
        self.rutas[id_nuevo] = nueva_ruta
        return nueva_ruta

    def modificar(self, id_ruta, origen=None, destino=None, longitud_km=None):
        if id_ruta not in self.rutas:
            return False, "Ruta no encontrada."
        
        ruta = self.rutas[id_ruta]
        
        if origen is not None:
            ruta.origen = origen
        elif destino is not None:
            ruta.destino = destino
        elif longitud_km is not None:
            ruta.longitud_km = longitud_km
            
        return True, ruta
    
    def eliminar(self, id_ruta):
        if id_ruta in self.rutas:
            del self.rutas[id_ruta]
            return True, "Ruta eliminada."
        return False, "Ruta no encontrada."

    def consultar(self, id_ruta):
        return self.rutas.get(id_ruta)
