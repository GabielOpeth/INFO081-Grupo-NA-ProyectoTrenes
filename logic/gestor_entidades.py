#Archivo de gestion de las entidades: gestor_entidades.py

#Importar Gestior a cada entidad correspondiente
from models.estacion import GestorEstaciones
from models.ruta import GestorRutas
from models.tren import GestorTrenes
from models.persona import GestorPersonas
#Asegúrense de que sus clases Estacion/Ruta/Tren tengan métodos consultar/crear.

class GestorEntidades:
    """Clase central para administrar todas las entidades y la lógica de inicio (RF04)."""

    def __init__(self):
        #Para iniciar los gestores
        self.gestor_estaciones = GestorEstaciones()
        self.gestor_rutas = GestorRutas()
        self.gestor_trenes = GestorTrenes()
        self.gestor_personas = GestorPersonas()
        
        #Un atributo a los RF01/RF02 (reseva de vias)
        self.reservas_vias = {} 
        
    #Accesos necesarios para la simulacion
    def obtener_tren(self, id_o_nombre):
        # Por ahora, asumimos que devuelve el primero si se busca por nombre placeholder en motor_simulacion.py
        for tren in self.gestor_trenes.trenes.values():
            if tren.nombre == id_o_nombre:
                return tren
            if str(tren.id) == str(id_o_nombre):
                return tren
        return None

    def obtener_estacion(self, id_o_nombre):
        for estacion in self.gestor_estaciones.estaciones.values():
            if estacion.nombre == id_o_nombre:
                return estacion
            if str(estacion.id) == str(id_o_nombre):
                return estacion
        return None

    # Implementación de la Lógica de Carga Inicial (RF04 - Anexo 1)
    def cargar_datos_iniciales_rf04(self):
        """Transfiere datos del Anexo 1 a los gestores de entidades."""
        print("Cargando datos iniciales de Estaciones, Rutas y Trenes (RF04)...")
        
        # *Asumiendo* que Estacion tiene un atributo 'vias' (Diccionario con orientación/estado)
        # 1. Estaciones (Población, Vías)
        santiago = self.gestor_estaciones.crear("Estación Central (Santiago)", 8242459, {'Norte': 'Libre', 'Sur': 'Libre', 'Rotacion': 'Libre'})
        rancagua = self.gestor_estaciones.crear("Rancagua", 274407, {'Norte': 'Libre', 'Sur': 'Libre', 'Rotacion': 'Libre'})
        talca = self.gestor_estaciones.crear("Talca", 242344, {'Norte': 'Libre', 'Sur': 'Libre', 'Rotacion': 'Libre'})
        chillan = self.gestor_estaciones.crear("Chillán", 204091, {'Norte': 'Libre', 'Sur': 'Libre', 'Rotacion': 'Libre'})
        
        # 2. Rutas (Origen/Destino, Longitud_km)
        self.gestor_rutas.crear(santiago, rancagua, 87) 
        self.gestor_rutas.crear(rancagua, santiago, 87)
        self.gestor_rutas.crear(rancagua, talca, 200)
        self.gestor_rutas.crear(talca, rancagua, 200)
        self.gestor_rutas.crear(talca, chillan, 180)
        self.gestor_rutas.crear(chillan, talca, 180)
        # Faltan Rutas: Santiago-Chillán, Chillán-Santiago (vía Talca y Rancagua)
        
        # 3. Trenes (Velocidad, Nombre, Vagones)
        # Vagones debe ser una lista de capacidades [Capacidad_Vagon1, ...]
        self.gestor_trenes.crear(160, "Tren BMU", [118, 118]) # 236 pasajeros total
        self.gestor_trenes.crear(120, "Tren EMU – EFE SUR", [100, 100]) # Capacidad asumida

        # Mínimos stubs para que el motor avance:
    def mover_tren_a_ruta(self, tren, ruta): pass
    def procesar_llegada_tren(self, tren, estacion): pass
    def obtener_proxima_ruta(self, estacion, tren): return self.gestor_rutas.consultar(1) # Stub
    def generar_demanda(self, estacion_id): pass

# Deje el resto de sus clases MotorSimulacion/MotorSimulacion en los archivos correspondientes
# El archivo original contenía una clase MotorSimulacion muy básica que ahora se ignora.