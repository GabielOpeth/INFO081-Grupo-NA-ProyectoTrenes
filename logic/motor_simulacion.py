import datetime as dt
import heapq 

# --- CLASES INTERNAS DE EVENTOS ---
class TipoEvento:
    SALIDA_TREN = 1
    LLEGADA_TREN = 2
    GENERAR_DEMANDA = 3

class Evento:
    def __init__(self, ocurrencia, nombre, datos, prioridad=1):
        self.ocurrencia = ocurrencia
        self.nombre = nombre
        self.datos = datos
        self.prioridad = prioridad
        self.tipo = self._asignar_tipo(nombre)

    def _asignar_tipo(self, nombre):
        if nombre == "SALIDA_TREN": return TipoEvento.SALIDA_TREN
        if nombre == "LLEGADA_TREN": return TipoEvento.LLEGADA_TREN
        if nombre == "GENERAR_DEMANDA": return TipoEvento.GENERAR_DEMANDA
        return 0

    def __lt__(self, other):
        return self.ocurrencia < other.ocurrencia

class LineaDeEventosSimple:
    def __init__(self, fecha_inicio):
        self.cola_eventos = []
        self.fecha_actual = fecha_inicio

    def insertar_evento_futuro(self, evento):
        heapq.heappush(self.cola_eventos, evento)

    def obtener_proximos(self, eliminar=True):
        if not self.cola_eventos: return []
        primer = self.cola_eventos[0]
        hora = primer.ocurrencia
        procesar = []
        while self.cola_eventos and self.cola_eventos[0].ocurrencia == hora:
            if eliminar: procesar.append(heapq.heappop(self.cola_eventos))
            else: 
                procesar.append(self.cola_eventos[0])
                break
        return procesar

    def consumir_eventos(self, eventos, historial=True):
        if eventos: self.fecha_actual = eventos[0].ocurrencia
        return self.fecha_actual

# --- MOTOR PRINCIPAL ---

class MotorSimulacion:
    def __init__(self, gestor_entidades, estado_simulacion):
        self.gestor_entidades = gestor_entidades
        self.estado_simulacion = estado_simulacion
        
        try:
            self.fecha_actual = dt.datetime(2015, 3, 1, 7, 0, 0)
        except:
            self.fecha_actual = dt.datetime.now()
            
        self.linea_eventos = LineaDeEventosSimple(self.fecha_actual)
        print(f"Motor listo. Hora: {self.fecha_actual}")

    def _calcular_tiempo_viaje(self, tren, ruta) -> dt.timedelta:
        vel = tren.velocidad if tren.velocidad > 0 else 80
        segundos = (ruta.longitud_km / vel) * 3600
        return dt.timedelta(seconds=int(segundos))

    def iniciar_simulacion(self):
        print("--- Iniciando Simulación ---")
        
        # 1. Programar Tren 1 (BMU) - Ida
        tren_bmu = self.gestor_entidades.obtener_tren("Tren BMU")
        ruta_ida = self.gestor_entidades.gestor_rutas.consultar(1) # Santiago -> Rancagua
        
        if tren_bmu and ruta_ida:
            t_salida = self.fecha_actual + dt.timedelta(minutes=5)
            self.linea_eventos.insertar_evento_futuro(Evento(t_salida, "SALIDA_TREN", 
                {'tren_id': tren_bmu.id, 'ruta': ruta_ida, 'estacion_origen_id': ruta_ida.origen.id}))
            print(f"✅ Tren BMU programado para {t_salida.time()}")

        # 2. Programar Tren 2 (EMU) - Vuelta
        tren_emu = self.gestor_entidades.obtener_tren("Tren EMU")
        ruta_vuelta = self.gestor_entidades.gestor_rutas.consultar(2) # Rancagua -> Santiago
        
        if tren_emu and ruta_vuelta:
            t_salida_2 = self.fecha_actual + dt.timedelta(minutes=20) # Sale 15 min después
            self.linea_eventos.insertar_evento_futuro(Evento(t_salida_2, "SALIDA_TREN", 
                {'tren_id': tren_emu.id, 'ruta': ruta_vuelta, 'estacion_origen_id': ruta_vuelta.origen.id}))
            print(f"✅ Tren EMU programado para {t_salida_2.time()}")

        # 3. Generar Demanda
        t_demanda = self.fecha_actual + dt.timedelta(minutes=2)
        self.linea_eventos.insertar_evento_futuro(Evento(t_demanda, "GENERAR_DEMANDA", 
            {'estacion_id': 'todas'}, prioridad=2))
        print(f"✅ Generación de pasajeros programada.")

    def avanzar_turno(self):
        eventos = self.linea_eventos.obtener_proximos()
        if not eventos: return False

        nueva_fecha = self.linea_eventos.consumir_eventos(eventos)
        self.fecha_actual = nueva_fecha
        self.estado_simulacion.hora_actual = self.fecha_actual.strftime("%H:%M:%S")
        
        print(f"⏱️ Hora: {self.estado_simulacion.hora_actual}")
        pausa = False

        for ev in eventos:
            if ev.tipo in [1, 2]: pausa = True 

            if ev.nombre == "GENERAR_DEMANDA":
                self.gestor_entidades.generar_demanda(ev.datos['estacion_id'])
                prox = self.fecha_actual + dt.timedelta(minutes=15)
                self.linea_eventos.insertar_evento_futuro(Evento(prox, "GENERAR_DEMANDA", ev.datos))

            elif ev.nombre == "SALIDA_TREN":
                tren = self.gestor_entidades.obtener_tren(ev.datos['tren_id'])
                ruta = ev.datos['ruta']
                self.gestor_entidades.mover_tren_a_ruta(tren, ruta)
                
                llegada = self.fecha_actual + self._calcular_tiempo_viaje(tren, ruta)
                self.linea_eventos.insertar_evento_futuro(Evento(llegada, "LLEGADA_TREN", 
                    {'tren_id': tren.id, 'estacion_destino_id': ruta.destino.id, 'ruta': ruta}))

            elif ev.nombre == "LLEGADA_TREN":
                tren = self.gestor_entidades.obtener_tren(ev.datos['tren_id'])
                est = self.gestor_entidades.obtener_estacion(ev.datos['estacion_destino_id'])
                self.gestor_entidades.procesar_llegada_tren(tren, est)
                
                salida = self.fecha_actual + dt.timedelta(minutes=10)
                prox_ruta = self.gestor_entidades.obtener_proxima_ruta(est, tren)
                self.linea_eventos.insertar_evento_futuro(Evento(salida, "SALIDA_TREN", 
                    {'tren_id': tren.id, 'ruta': prox_ruta, 'estacion_origen_id': est.id}))

        return pausa