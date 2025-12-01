#Archivo de gestion de las entidades: gestor_entidades.py

#Importar Gestior a cada entidad correspondiente
from models.estacion import GestorEstaciones
from models.ruta import GestorRutas
from models.tren import GestorTrenes
from models.persona import GestorPersonas
#Asegúrense de que sus clases Estacion/Ruta/Tren tengan métodos consultar/crear.

class GestorEntidades:
    #Clase central para administrar todas las entidades y la lógica de inicio (RF04).

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
    
    def obtener_ruta(self, id_o_nombre):
    #Retorna la primera ruta (ID 1), asumiendo que es la inicial (Santiago -> Rancagua)
    #Usamos el consultar por ID, que es lo más seguro después de cargar RF04.
    return self.gestor_rutas.consultar(1)

    #Esta seccion va a cargar los datos pedidos en el Anexo 1 del proyecto
    def cargar_datos_iniciales_rf04(self):
        #Transfiere datos del Anexo 1 a los gestores de entidades.
        print("Cargando datos iniciales de Estaciones, Rutas y Trenes (RF04)...")
        
        #Consideramos que lo màs prudente era usar diccionarios para cargar los datos
        #1ro. Estaciones (Poblaciones, Vías)
        santiago = self.gestor_estaciones.crear("Estación Central (Santiago)", 8242459, {'Norte': 'Libre', 'Sur': 'Libre', 'Rotacion': 'Libre'})
        rancagua = self.gestor_estaciones.crear("Rancagua", 274407, {'Norte': 'Libre', 'Sur': 'Libre', 'Rotacion': 'Libre'})
        talca = self.gestor_estaciones.crear("Talca", 242344, {'Norte': 'Libre', 'Sur': 'Libre', 'Rotacion': 'Libre'})
        chillan = self.gestor_estaciones.crear("Chillán", 204091, {'Norte': 'Libre', 'Sur': 'Libre', 'Rotacion': 'Libre'})
        
        #2do. Rutas (Origen o Destino, Longitud en km)
        self.gestor_rutas.crear(santiago, rancagua, 87) 
        self.gestor_rutas.crear(rancagua, santiago, 87)
        self.gestor_rutas.crear(rancagua, talca, 200)
        self.gestor_rutas.crear(talca, rancagua, 200)
        self.gestor_rutas.crear(talca, chillan, 180)
        self.gestor_rutas.crear(chillan, talca, 180)
        #Faltan Rutas: Santiago-Chillan, Chillan-Santiago (vía Talca y Rancagua)
        
        #3ro. Trenes (Velocidad, Nombre, Vagones)
        #Vagones son una lista de las capacidades cuyo orden es (Vagon_n, capacidad)
        self.gestor_trenes.crear(160, "Tren BMU", [118, 118]) # 236 pasajeros total
        self.gestor_trenes.crear(120, "Tren EMU – EFE SUR", [100, 100]) # Capacidad asumida

        #Funciones de placeholder minimas con cambio de estado
    def mover_tren_a_ruta(self, tren, ruta):
        # Lógica mínima: el tren ya no está en una estación y está en la ruta.
        tren.ruta_actual = ruta
        tren.ubicacion_actual = "En ruta: " + str(ruta.id) # Actualiza la ubicación del tren
        tren.distancia_recorrida_ruta = 0 
        
    def procesar_llegada_tren(self, tren, estacion): 
        # Lógica mínima: el tren llegó y está en la estación de destino.
        tren.ruta_actual = None
        tren.ubicacion_actual = estacion # La ubicación ahora es el objeto Estacion
        tren.distancia_recorrida_ruta = 0
        
    def obtener_proxima_ruta(self, estacion, tren): 
        # Stub: Siempre devuelve la ruta 1 para crear un ciclo infinito de prueba simple.
        return self.gestor_rutas.consultar(1) 
        
    def generar_demanda(self, estacion_id): 
        pass # Este es el placeholder para el RF05/RF06.