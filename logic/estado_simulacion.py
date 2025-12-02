

from datetime import datetime
import datetime as dt
import json


from .gestor_entidades import GestorEntidades
from models.estacion import Estacion
from models.tren import Tren
from models.ruta import Ruta
from models.persona import Persona
from .sistema_guardado import SistemaDeGuardado

class EstadoSimulacion:
    def __init__(self):
        self.hora_actual = str(datetime.now().strftime("%H:%M:%S"))
        self.gestor_entidades = GestorEntidades()
        self.linea_eventos = []

    def to_serializable(self):
        return {
            "hora_actual": self.hora_actual,
            "entidades": {
                "estaciones": [e.to_dict() for e in self.gestor_entidades.gestor_estaciones.obtener_todas()],
                "rutas": [r.to_dict() for r in self.gestor_entidades.gestor_rutas.obtener_todas()],
                "trenes": [t.to_dict() for t in self.gestor_entidades.gestor_trenes.obtener_todos()],
                "personas": [p.to_dict() for p in self.gestor_entidades.gestor_personas.personas.values()] 
            },
            "eventos": self.linea_eventos 
        }

    @staticmethod
    def from_serializable(data):
        """
        [RF08] Reconstruye el EstadoSimulacion desde un diccionario cargado.
        Sigue el orden: Limpieza -> Estaciones/Trenes -> Rutas -> Personas.
        """
        nuevo_estado = EstadoSimulacion()
        nuevo_estado.hora_actual = data.get("hora_actual", "07:00:00")
  
        gestor = nuevo_estado.gestor_entidades
        gestor.gestor_estaciones.estaciones.clear()
        gestor.gestor_trenes.trenes.clear()
        gestor.gestor_rutas.rutas.clear()
        gestor.gestor_personas.personas.clear()

        entidades_data = data.get('entidades', {})


        

        for est_data in entidades_data.get('estaciones', []):

            nueva_estacion = Estacion(
                est_data['id'], 
                est_data['nombre'], 
                est_data['poblacion'], 
                est_data['vias']
            )

            nueva_estacion.flujo_acumulado = est_data.get('flujo_acumulado', 0)
            nueva_estacion.pasajeros_esperando = est_data.get('pasajeros_esperando', 0)
            

            gestor.gestor_estaciones.estaciones[nueva_estacion.id] = nueva_estacion


        for tren_data in entidades_data.get('trenes', []):
            nuevo_tren = Tren(
                tren_data['id'],
                tren_data['velocidad'],
                tren_data['nombre'],
                tren_data['vagones']
            )

            gestor.gestor_trenes.trenes[nuevo_tren.id] = nuevo_tren

        
        for ruta_data in entidades_data.get('rutas', []):
            origen_id = ruta_data['origen_id']
            destino_id = ruta_data['destino_id']
            

            obj_origen = gestor.gestor_estaciones.consultar(origen_id)
            obj_destino = gestor.gestor_estaciones.consultar(destino_id)
            
            if obj_origen and obj_destino:
                nueva_ruta = Ruta(
                    ruta_data['id'],
                    obj_origen, 
                    obj_destino, 
                    ruta_data['longitud_km']
                )
                gestor.gestor_rutas.rutas[nueva_ruta.id] = nueva_ruta


        
        for p_data in entidades_data.get('personas', []):

            try:
                tiempo_dt = dt.datetime.fromisoformat(p_data['tiempo_llegada'])
            except ValueError:
                tiempo_dt = dt.datetime.now() 

            nueva_persona = Persona(
                p_data['id'],
                p_data['origen_id'],
                p_data['destino_id'],
                tiempo_dt 
            )
            nueva_persona.viajando = p_data.get('viajando', False)
            nueva_persona.en_estacion = p_data.get('en_estacion', True)
            
            gestor.gestor_personas.personas[nueva_persona.id] = nueva_persona
        return nuevo_estado