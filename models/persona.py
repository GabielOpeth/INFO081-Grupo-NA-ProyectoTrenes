class Persona:
    def __init__(self, id, origen_id, destino_id, tiempo_llegada_simulacion, viajando=False):
        self.id = id
        self.origen_id = origen_id
        self.destino_id = destino_id
        self.tiempo_llegada_simulacion = tiempo_llegada_simulacion
        self.viajando = viajando
        self.en_estacion = True

    def __repr__(self):
        estado = "Viajando" if self.viajando else ("En Estación" if self.en_estacion else "Terminó Viaje")
        return f"Persona(ID: {self.id}, Origen: {self.origen_id}, Destino: {self.destino_id}, Estado: {estado})"

    def dick(self):
        return {
            "id": self.id,
            "origen_id": self.origen_id,
            "destino_id": self.destino_id,
            "tiempo_llegada_simulacion": self.tiempo_llegada_simulacion,
            "viajando": self.viajando,
            "en_estacion": self.en_estacion
        }

class GestorPersonas:
    def __init__(self):
        self.personas = {}
        self.next_id = 1

    def _obtener_id(self):
        id_gen = self.next_id
        self.next_id += 1
        return id_gen

    def crear(self, origen_id, destino_id, tiempo_llegada_simulacion):
        id_nuevo = self._obtener_id()
        nueva_persona = Persona(id_nuevo, origen_id, destino_id, tiempo_llegada_simulacion)
        self.personas[id_nuevo] = nueva_persona
        return nueva_persona

    def modificar_estado(self, id_persona, viajando=None, en_estacion=None):
        if id_persona not in self.personas:
            return False, "Persona no encontrada."
        
        persona = self.personas[id_persona]
        
        if viajando is not None:
            persona.viajando = viajando
        if en_estacion is not None:
            persona.en_estacion = en_estacion
            
        return True, persona
    
    def eliminar(self, id_persona):
        if id_persona in self.personas:
            del self.personas[id_persona]
            return True, "Persona eliminada."
        return False, "Persona no encontrada."

    def consultar(self, id_persona):
        return self.personas.get(id_persona)