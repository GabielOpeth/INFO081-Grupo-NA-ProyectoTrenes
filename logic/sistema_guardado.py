from datetime import datetime,time
import json
from .estado_simulacion import EstadoSimulacion  #Archivo de estado_simulacion.py


class SistemaDeGuardado:
    
    def guardar_simulacion(self, estado_simulacion, nombre_archivo=None):
       
        data_a_guardar = {
            "hora_actual": estado_simulacion.hora_actual,
            "trenes_activos": ["TrenRandom", "TREN_VIALACTEA"], #Desconocido por el momento
            "estaciones": len("DESCONOCIDAS") #Desconocido de momento, es para la simulacion
        }
        
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(data_a_guardar, archivo, indent=4)
        print(f"Datos guardados exitosamente en {nombre_archivo}")

#-------------------------------------------------------------------------------------------------------------------------

    def cargar_simulacion(self, nombre_archivo=None):
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos_cargados = json.load(archivo)
            print(f"Datos cargados: {datos_cargados}")
                
            hora = datos_cargados.get("hora_actual", "00:00")
            print(f"La hora actual cargada es: {hora}")
            return datos_cargados

if __name__=="__main__":
    main()