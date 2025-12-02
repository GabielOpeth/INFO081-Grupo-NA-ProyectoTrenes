#El presente archivo corresponde al estado de simulacion del Proyecto: estado_simulacion.py

#Estas son algunas importaciones necesarias para el funcionamiento del proyecto, tales como:
from datetime import datetime   #Para fechas
import datetime as dt           # ""
import json                     #Esencial para el sistema de guardado y carga de la simulacion (usa formato json)

#Estas son algunas importaciones del resto de archivos del proyecto (modularizacion)
from .gestor_entidades import GestorEntidades #Ubicado en logic, porsia
from models.estacion import Estacion          #Corresponde a modelos necesarios basicos
from models.tren import Tren                  # ""
from models.ruta import Ruta                  # ""
from models.persona import Persona            # ""

class EstadoSimulacion:
    def __init__(self):
        self.hora_actual = str(datetime.now().strftime("%H:%M:%S"))
        self.gestor_entidades = GestorEntidades()
        self.linea_eventos = []

    def to_serializable(self):
        """
        [RF08] Prepara el objeto EstadoSimulacion para ser guardado como JSON.
        """
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