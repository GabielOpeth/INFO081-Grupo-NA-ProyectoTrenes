from datetime import datetime,time
import json


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


# ----- Nota del desarrollador -----
# Más adelante en la siguiente entrega, los estados de simulación se importarán desde el archivo.py

class EstadoSimulacion:
    def __init__(self):
        self.hora_actual = str(datetime.now())
def prueba():
    #Funcion de prueba, se planea implementar algo similar en la interfaz de carga datos
    #GUARDAR
    guardador = SistemaDeGuardado()
    estado = EstadoSimulacion()
    nombre=input("Ingresa nombre del archivo:")
    real=nombre+".json"
    guardador.guardar_simulacion(estado,real)

    #CARGAR
    guardador = SistemaDeGuardado()
    data_recuperada = guardador.cargar_simulacion(real)
def main():
    prueba()



if __name__=="__main__":
    main()