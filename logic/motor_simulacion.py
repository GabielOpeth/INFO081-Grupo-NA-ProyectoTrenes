# motor_simulacion.py
import datetime as dt
import heapq # Usaremos esto para una cola de prioridad simple

# --- CLASES INTERNAS DE EVENTOS (Para que funcione sin dependencias externas) ---
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

    # Esto permite comparar eventos por fecha (necesario para la fila)
    def __lt__(self, other):
        return self.ocurrencia < other.ocurrencia

class LineaDeEventosSimple:
    def __init__(self, fecha_inicio):
        self.cola_eventos = []
        self.fecha_actual = fecha_inicio

    def insertar_evento_futuro(self, evento):
        heapq.heappush(self.cola_eventos, evento)

    def obtener_proximos(self, eliminar=True):
        if not self.cola_eventos:
            return []
        
        # Miramos el primer evento
        primer_evento = self.cola_eventos[0]
        hora_evento = primer_evento.ocurrencia
        
        # Sacamos todos los eventos que ocurran a esa misma hora
        eventos_a_procesar = []
        
        # Mientras haya eventos y sean a la misma hora que el primero...
        while self.cola_eventos and self.cola_eventos[0].ocurrencia == hora_evento:
            if eliminar:
                eventos_a_procesar.append(heapq.heappop(self.cola_eventos))
            else:
                eventos_a_procesar.append(self.cola_eventos[0])
                break # Si no eliminamos, solo miramos el primero para chequear
        
        return eventos_a_procesar

    def consumir_eventos(self, eventos, historial=True):
        if eventos:
            # La nueva fecha del sistema es la fecha de estos eventos
            self.fecha_actual = eventos[0].ocurrencia
        return self.fecha_actual

# --- CLASE MOTOR PRINCIPAL ---

class MotorSimulacion:
    
    def __init__(self, gestor_entidades, estado_simulacion):
        self.gestor_entidades = gestor_entidades
        self.estado_simulacion = estado_simulacion

        # Inicialización de Fecha (07:00:00)
        HORA_INICIAL_DEFAULT = "07:00:00"
        FECHA_BASE = "01-03-2015"
        FORMATO = "%d-%m-%Y %H:%M:%S"

        hora_str = getattr(self.estado_simulacion, 'hora_actual', HORA_INICIAL_DEFAULT)
        # Si viene vacía o rara, forzamos default
        if not hora_str or len(hora_str) < 5: 
            hora_str = HORA_INICIAL_DEFAULT

        # Intentamos armar la fecha completa
        try:
            # Si hora_str ya trae fecha, intentamos parsear directo
            if "2015" in hora_str:
                 fecha_inicial_dt = dt.datetime.strptime(hora_str, FORMATO) # Formato completo
            else:
                 # Si solo es hora, pegamos la fecha base
                 fecha_base_str = f"{FECHA_BASE} {hora_str}"
                 fecha_inicial_dt = dt.datetime.strptime(fecha_base_str, FORMATO)
        except ValueError:
            # Fallback seguro
            fecha_inicial_dt = dt.datetime(2015, 3, 1, 7, 0, 0)
        
        # Usamos nuestra clase interna simple
        self.linea_eventos = LineaDeEventosSimple(fecha_inicial_dt)
        self.fecha_actual = fecha_inicial_dt
        
        print(f"Motor Inicializado. Hora de inicio: {self.fecha_actual}")

    def _calcular_tiempo_viaje(self, tren, ruta) -> dt.timedelta:
        velocidad_kmh = tren.velocidad if tren and tren.velocidad > 0 else 80 
        tiempo_horas = ruta.longitud_km / velocidad_kmh
        segundos = tiempo_horas * 3600 
        return dt.timedelta(seconds=int(segundos))

    def iniciar_simulacion(self):
        print("--- Iniciando Simulación ---")
        # 1. Asegurar datos
        self.gestor_entidades.cargar_datos_iniciales_rf04()
        
        try:
            # 2. Programar primer evento (Salida en 5 mins)
            tren_inicial = self.gestor_entidades.obtener_tren("Tren_BMU")
            # Obtenemos cualquier ruta válida para empezar
            ruta_inicial = self.gestor_entidades.obtener_ruta(1) 
            
            if tren_inicial and ruta_inicial:
                tiempo_salida = self.fecha_actual + dt.timedelta(minutes=5)
                
                primer_evento = Evento(
                    ocurrencia=tiempo_salida, 
                    nombre="SALIDA_TREN", 
                    datos={'tren_id': tren_inicial.id, 'ruta': ruta_inicial, 'estacion_origen_id': ruta_inicial.origen.id}
                )
                self.linea_eventos.insertar_evento_futuro(primer_evento)
                print(f"✅ Evento programado: SALIDA_TREN a las {tiempo_salida.time()}")
            else:
                print("⚠️ No se encontraron trenes o rutas para iniciar eventos.")

        except Exception as e:
            print(f"⛔ Error al programar eventos iniciales: {e}")

    def avanzar_turno(self):
        """
        Avanza el reloj hasta el siguiente evento y lo procesa.
        """
        # 1. Ver qué eventos tocan ahora
        eventos_a_procesar = self.linea_eventos.obtener_proximos(eliminar=True)
        
        if not eventos_a_procesar:
            print("No hay más eventos pendientes.")
            return False

        # 2. Avanzar el reloj
        fecha_proxima = self.linea_eventos.consumir_eventos(eventos_a_procesar)
        self.fecha_actual = fecha_proxima
        # Actualizamos el estado global para que la UI lo lea
        self.estado_simulacion.hora_actual = self.fecha_actual.strftime("%H:%M:%S")
        
        print(f"⏱️ Avanzando a: {self.estado_simulacion.hora_actual}")
        
        debe_pausar = False
        
        # 3. Procesar lógica
        for evento in eventos_a_procesar:
            print(f"   Ejecutando: {evento.nombre}")
            
            if evento.tipo in [TipoEvento.LLEGADA_TREN, TipoEvento.SALIDA_TREN]: 
                debe_pausar = True

            if evento.nombre == "SALIDA_TREN":
                tren = self.gestor_entidades.obtener_tren(evento.datos['tren_id'])
                ruta = evento.datos['ruta']
                
                if tren and ruta:
                    self.gestor_entidades.mover_tren_a_ruta(tren, ruta)
                    
                    # Programar Llegada
                    tiempo_viaje = self._calcular_tiempo_viaje(tren, ruta)
                    tiempo_llegada = self.fecha_actual + tiempo_viaje
                    
                    nuevo_evento = Evento(
                        ocurrencia=tiempo_llegada, 
                        nombre="LLEGADA_TREN", 
                        datos={'tren_id': tren.id, 'estacion_destino_id': ruta.destino.id, 'ruta': ruta}
                    )
                    self.linea_eventos.insertar_evento_futuro(nuevo_evento)
                    print(f"   -> Próximo: LLEGADA a las {tiempo_llegada.time()}")

            elif evento.nombre == "LLEGADA_TREN":
                tren = self.gestor_entidades.obtener_tren(evento.datos['tren_id'])
                estacion = self.gestor_entidades.obtener_estacion(evento.datos['estacion_destino_id'])
                
                if tren and estacion:
                    self.gestor_entidades.procesar_llegada_tren(tren, estacion)
                    
                    # Programar siguiente Salida (Rotación)
                    tiempo_salida = self.fecha_actual + dt.timedelta(minutes=10) # 10 min de espera
                    proxima_ruta = self.gestor_entidades.obtener_proxima_ruta(estacion, tren)
                    
                    if proxima_ruta:
                        nuevo_evento = Evento(
                            ocurrencia=tiempo_salida, 
                            nombre="SALIDA_TREN", 
                            datos={'tren_id': tren.id, 'ruta': proxima_ruta, 'estacion_origen_id': estacion.id}
                        )
                        self.linea_eventos.insertar_evento_futuro(nuevo_evento)
                        print(f"   -> Próximo: SALIDA a las {tiempo_salida.time()}")

        return debe_pausar