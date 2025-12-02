import random
import datetime as dt
from models.estacion import GestorEstaciones
from models.ruta import GestorRutas
from models.tren import GestorTrenes
from models.persona import GestorPersonas

class GestorEntidades:
    def __init__(self):
        self.gestor_estaciones = GestorEstaciones()
        self.gestor_rutas = GestorRutas()
        self.gestor_trenes = GestorTrenes()
        self.gestor_personas = GestorPersonas()
        self.reservas_vias = {} 

    def obtener_tren(self, id_o_nombre):
        for tren in self.gestor_trenes.trenes.values():
            if tren.nombre == id_o_nombre: return tren
            if str(tren.id) == str(id_o_nombre): return tren
        return None

    def obtener_estacion(self, id_o_nombre):
        for estacion in self.gestor_estaciones.estaciones.values():
            if estacion.nombre == id_o_nombre: return estacion
            if str(estacion.id) == str(id_o_nombre): return estacion
        return None
    
    def obtener_ruta(self, id_ruta):
        # Corrección: Ahora busca la ruta real por ID
        return self.gestor_rutas.consultar(id_ruta)

    def cargar_datos_iniciales_rf04(self):
        print("Cargando datos iniciales (RF04)...")
        # 1. Estaciones
        stgo = self.gestor_estaciones.crear("Estación Central", 8000000, {'Norte': 'Libre'})
        rancagua = self.gestor_estaciones.crear("Rancagua", 250000, {'Norte': 'Libre'})
        talca = self.gestor_estaciones.crear("Talca", 240000, {'Norte': 'Libre'})
        chillan = self.gestor_estaciones.crear("Chillán", 200000, {'Norte': 'Libre'})
        
        # 2. Rutas
        self.gestor_rutas.crear(stgo, rancagua, 87) # ID 1
        self.gestor_rutas.crear(rancagua, stgo, 87) # ID 2
        self.gestor_rutas.crear(rancagua, talca, 150)
        self.gestor_rutas.crear(talca, chillan, 100)
        
        # 3. Trenes
        self.gestor_trenes.crear(160, "Tren BMU", [100, 100]) 
        self.gestor_trenes.crear(120, "Tren EMU", [80, 80]) 

    # --- LÓGICA DE MOVIMIENTO Y PERSONAS ---

    def mover_tren_a_ruta(self, tren, ruta):
        tren.ruta_actual = ruta
        tren.ubicacion_actual = f"En ruta a {ruta.destino.nombre}"
        
    def procesar_llegada_tren(self, tren, estacion): 
        tren.ruta_actual = None
        tren.ubicacion_actual = estacion
        
        # 1. Bajar Pasajeros
        for p in self.gestor_personas.personas.values():
            if p.viajando: 
                p.viajando = False
                p.en_estacion = False
        
        # 2. Subir Pasajeros
        capacidad = tren.capacidad_total()
        esperando = estacion.pasajeros_esperando
        suben = min(esperando, capacidad)
        
        estacion.pasajeros_esperando -= suben
        
        contador = 0
        for p in self.gestor_personas.personas.values():
            if contador >= suben: break
            if p.origen_id == estacion.id and p.en_estacion:
                p.viajando = True
                p.en_estacion = False
                contador += 1
                
        print(f"   🚉 {tren.nombre} en {estacion.nombre}: Bajaron todos, subieron {suben}.")

    def obtener_proxima_ruta(self, estacion, tren): 
        todas = self.gestor_rutas.obtener_todas()
        for r in todas:
            if r.origen.id == estacion.id:
                return r
        return self.gestor_rutas.consultar(1)
        
    def generar_demanda(self, estacion_id): 
        """Crea personas aleatorias en las estaciones"""
        estaciones_destino = self.gestor_estaciones.obtener_todas()
        targets = self.gestor_estaciones.obtener_todas() if estacion_id == 'todas' else [self.gestor_estaciones.consultar(estacion_id)]
        
        total_nuevos = 0
        for est in targets:
            if not est: continue
            cantidad = random.randint(5, 15)
            total_nuevos += cantidad
            
            for _ in range(cantidad):
                destino = random.choice(estaciones_destino)
                while destino.id == est.id and len(estaciones_destino) > 1:
                    destino = random.choice(estaciones_destino)
                
                self.gestor_personas.crear(est.id, destino.id, dt.datetime.now())
                est.pasajeros_esperando += 1
        
        print(f"   👥 Se generaron {total_nuevos} nuevos pasajeros esperando.")