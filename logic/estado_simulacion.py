from .sistema_guardado_old import SistemaDeGuardado
import json
from datetime import datetime, time

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