from datetime import datetime, time
import json
# Importar la clase central que creaste
from .gestor_entidades import GestorEntidades 
# Importamos dt.datetime para que Persona 2 pueda manejar la serialización de fechas de Personas
import datetime as dt 
# Importamos SistemaDeGuardado para las funciones de prueba (si las usan)
from .sistema_guardado import SistemaDeGuardado 

class EstadoSimulacion:
    def __init__(self):
        self.hora_actual = str(datetime.now())
        self.gestor_entidades = GestorEntidades() # <--- ¡CLAVE RF02! Contiene Trenes, Estaciones, Rutas, etc.
        self.linea_eventos = [] # Placeholder inicial para la línea temporal (RF09)
        
    def to_serializable(self):
        """
        [RF08] Prepara el objeto EstadoSimulacion para ser guardado como JSON.
        Convierte todos los objetos complejos (Estaciones, Rutas, Trenes) 
        a su representación de diccionario serializable.
        """
        # Se asume que los modelos (Estacion, Ruta, Tren, Persona) tienen un método .to_dict()
        return {
            "hora_actual": self.hora_actual,
            "entidades": {
                # Utiliza obtener_todas/obtener_todos de tus gestores.
                "estaciones": [e.to_dict() for e in self.gestor_entidades.gestor_estaciones.obtener_todas()],
                "rutas": [r.to_dict() for r in self.gestor_entidades.gestor_rutas.obtener_todas()],
                "trenes": [t.to_dict() for t in self.gestor_entidades.gestor_trenes.obtener_todos()],
                "personas": [p.to_dict() for p in self.gestor_entidades.gestor_personas.personas.values()] 
            },
            # Persona 3 debe asegurar que los eventos sean serializables.
            "eventos": self.linea_eventos 
        }

    @staticmethod
    def from_serializable(data):
    #Crea instancia a base de datos cargados
    #Continua Alvaro
        nuevo_estado = EstadoSimulacion()
        nuevo_estado.hora_actual = data.get("hora_actual", str(datetime.now()))
        
        # ------------------------------------------------------------------
        # Lógica de reconstrucción (PENDIENTE de Persona 2):
        # 1. Borrar o reiniciar gestores de nuevo_estado.gestor_entidades
        # 2. Reconstruir ESTACIONES.
        # 3. Reconstruir TRENES.
        # 4. Reconstruir RUTAS (usando las Estaciones reconstruidas).
        # 5. Reconstruir PERSONAS.
        # ------------------------------------------------------------------
        
        return nuevo_estado
        
# -------------------------------------------------------------------------
# NOTA: Funciones de prueba originales dejadas abajo para compatibilidad
# -------------------------------------------------------------------------

def prueba():
    # Funcion de prueba, se planea implementar algo similar en la interfaz de carga datos
    # GUARDAR
    guardador = SistemaDeGuardado()
    estado = EstadoSimulacion()
    # Para probar la serialización, carga los datos iniciales
    estado.gestor_entidades.cargar_datos_iniciales_rf04()
    
    nombre=input("Ingresa nombre del archivo:")
    real=nombre+".json"
    
    # El método guardar_simulacion en sistema_guardado.py DEBE ser modificado
    # por Persona 2 para usar estado.to_serializable()
    # guardador.guardar_simulacion(estado,real) 
    
    # CARGAR
    # guardador = SistemaDeGuardado()
    # data_recuperada = guardador.cargar_simulacion(real)
    
def main():
    # prueba()
    # No corran la prueba hasta que Persona 2 haya actualizado sistema_guardado.py
    print("Prueba de EstadoSimulacion lista para ser implementada por Persona 2.")

if __name__=="__main__":
    main()