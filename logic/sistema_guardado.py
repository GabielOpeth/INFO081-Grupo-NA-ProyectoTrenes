
import json
import datetime as dt
from .estado_simulacion import EstadoSimulacion

class SistemaDeGuardado:

    def guardar_simulacion(self, estado_simulacion, nombre_archivo=None):
        """
        [RF08] Guarda el estado completo en un archivo JSON.
        """
        data_a_guardar = estado_simulacion.to_serializable()


        if not nombre_archivo.endswith(".json"):
            nombre_archivo += ".json"

        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(data_a_guardar, archivo, indent=4, default=str)
        
        print(f"✅ Datos guardados exitosamente en {nombre_archivo}")

    def cargar_simulacion(self, nombre_archivo=None):
 
        if not nombre_archivo.endswith(".json"):
            nombre_archivo += ".json"
            
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos_cargados = json.load(archivo)
            
        print(f"📂 Archivo leído. Iniciando reconstrucción del estado...")
        
        nuevo_estado = EstadoSimulacion.from_serializable(datos_cargados)
        
        print(f"✅ Estado reconstruido exitosamente. Hora: {nuevo_estado.hora_actual}")
        return nuevo_estado