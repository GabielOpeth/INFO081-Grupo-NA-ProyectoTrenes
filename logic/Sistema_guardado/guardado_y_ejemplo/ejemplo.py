#Aqui deben importar la clase con sus funciones del sistema de guardado que esta en la misma carpeta.
#Se crearan archivos .json que quedaran guardados aqui por ahora, hasta que haya mas orden.



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
    guardador.guardatos(estado,real)

    #CARGAR
    guardador = SistemaDeGuardado()
    data_recuperada = guardador.cargar_simulacion(real)
def main():
    prueba()

if __name__=="__main__":
    main()