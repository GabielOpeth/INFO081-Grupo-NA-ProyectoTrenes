import datetime as dt
#se importa la herramienta de tiempo(reloj y calendario).
from ppdc_event_manager import TipoEvento, Evento, LineaDeEventos #
#Algunas clases internas de eventos
class TipoEvento:
    SALIDA_TREN = 1
    LLEGADA_TREN = 2
    GENERAR_DEMANDA = 3

class Evento:
    def __init__(self, ocurrencia, nombre, datos, prioridad=1):
        self.ocurrencia = ocurrencia #¿Cuando va a pasar?
        self.nombre = nombre #¿Que va a pasar?
        self.datos = datos #Informacion(Que tren, que estacion, etc)
        self.prioridad = prioridad #Si dos eventos ocurren al mismo tiempo, ¿A cual se le da prioridad?
        self.tipo = self._asignar_tipo(nombre) #Etiqueta numerica

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
        self.cola_eventos.append(evento)
        self.cola_eventos.sort()

    def obtener_proximos(self, eliminar=True):
        if not self.cola_eventos:
            return []
            
        hora_proxima = self.cola_eventos[0].ocurrencia
        
        procesar = []
        eventos_futuros = []
        
        for evento in self.cola_eventos:
            if evento.ocurrencia == hora_proxima:
                procesar.append(evento)
            else:
                eventos_futuros.append(evento)
                
        if eliminar:
            self.cola_eventos = eventos_futuros
            
        return procesar
        
    def consumir_eventos(self, eventos, historial=True):
        if eventos: self.fecha_actual = eventos[0].ocurrencia
        return self.fecha_actual

class MotorSimulacion:
    def __init__(self, gestor_entidades, estado_simulacion):
        self.gestor_entidades = gestor_entidades
        self.estado_simulacion = estado_simulacion
        
        #inicilización del reloj interno
        try:
            self.fecha_actual = dt.datetime(2015, 3, 1, 7, 0, 0)
        except:
            self.fecha_actual = dt.datetime.now()

        #Linea de eventos:
        #Cola de prioridad de eventos futuros
        #Simulación discreta de evento.
            
        self.linea_eventos = LineaDeEventos(self.estado_simulacion, self.fecha_actual) 
        print(f"Motor listo. Hora: {self.fecha_actual}")

    def _calcular_tiempo_viaje(self, tren, ruta) -> dt.timedelta:
        vel = tren.velocidad if tren.velocidad > 0 else 80
        segundos = (ruta.longitud_km / vel) * 3600
        return dt.timedelta(seconds=int(segundos))
    
    #Formula usada, tiempo = distancia/velocidad.
    #Se asume que la velocidad es constante durante el viaje

    
    def _handle_generar_demanda(self, datos):
        #Funcion hecha para generar pasajeros
        #Crea entidades de pasajeros en las estaciones
        #Se agenda a si mismo cada 15 minutos para repetir el bucle de manera infinita.
        """Logica: loop de generacion de demanda. Debe reprogramar el proximo evento."""
        
        self.gestor_entidades.generar_demanda(datos['estacion_id'])
        
        prox = self.fecha_actual + dt.timedelta(minutes=15)
        
        self.linea_eventos.insertar_evento_futuro(
            Evento(TipoEvento.GENERAR_DEMANDA, prox, lambda: self._handle_generar_demanda(datos), prioridad=2)
        )

    def _handle_salida_tren(self, datos):

        #Evento recurrente:
        #Este evento genera la demanda y ademas
        #perpetua en el ciclo.
        """Logica: salida del tren. Crea el evento de llegada y pausa la simulación."""
        tren = self.gestor_entidades.obtener_tren(datos['tren_id'])
        ruta = datos['ruta']
        
        self.gestor_entidades.mover_tren_a_ruta(tren, ruta)
        
        llegada = self.fecha_actual + self._calcular_tiempo_viaje(tren, ruta)
        
        datos_llegada = {
            'tren_id': tren.id, 
            'estacion_destino_id': ruta.destino.id, 
            'ruta': ruta
        }

        self.linea_eventos.insertar_evento_futuro(
            Evento(TipoEvento.TREN_LLEGADA, llegada, lambda: self._handle_llegada_tren(datos_llegada))
        )
        
        self.estado_simulacion.debe_pausar = True

    def _handle_llegada_tren(self, datos):
        #Funcion(El tren llega)
        #Baja y sube gente(Gestor)
        #Decide proxima ruta
        #Anota en la agenda la siguiente salida
        """Logica: llegada del tren. Crea el evento de proxima salida y pausa la simulación."""
        tren = self.gestor_entidades.obtener_tren(datos['tren_id'])
        est = self.gestor_entidades.obtener_estacion(datos['estacion_destino_id'])
        
        self.gestor_entidades.procesar_llegada_tren(tren, est)
        
        salida = self.fecha_actual + dt.timedelta(minutes=10)
        
        prox_ruta = self.gestor_entidades.obtener_proxima_ruta(est, tren)
        
        datos_salida = {
            'tren_id': tren.id, 
            'ruta': prox_ruta, 
            'estacion_origen_id': est.id
        }

        self.linea_eventos.insertar_evento_futuro(
            Evento(TipoEvento.MODIFICACION_SISTEMA, salida, lambda: self._handle_salida_tren(datos_salida))
        )
        
        self.estado_simulacion.debe_pausar = True

    def iniciar_simulacion(self):
        #Busca los trenes y sus rutas iniciales
        #Primera generacion de pasajeros
        print("Iniciando Simulación...")
        
        tren_bmu = self.gestor_entidades.obtener_tren("Tren BMU")
        ruta_ida = self.gestor_entidades.gestor_rutas.consultar(1)
        
        if tren_bmu and ruta_ida:
            t_salida = self.fecha_actual + dt.timedelta(minutes=5)
            datos_salida_1 = {'tren_id': tren_bmu.id, 'ruta': ruta_ida, 'estacion_origen_id': ruta_ida.origen.id}
            
            self.linea_eventos.insertar_evento_futuro(
                Evento(TipoEvento.GENERAR_DEMANDA, t_salida, lambda: self._handle_salida_tren(datos_salida_1), prioridad=1)
            )
            print(f"Tren BMU programado para {t_salida.time()}")

        tren_emu = self.gestor_entidades.obtener_tren("Tren EMU")
        ruta_vuelta = self.gestor_entidades.gestor_rutas.consultar(2)
        
        if tren_emu and ruta_vuelta:
            t_salida_2 = self.fecha_actual + dt.timedelta(minutes=20)
            datos_salida_2 = {'tren_id': tren_emu.id, 'ruta': ruta_vuelta, 'estacion_origen_id': ruta_vuelta.origen.id}

            self.linea_eventos.insertar_evento_futuro(
                Evento(TipoEvento.GENERAR_DEMANDA, t_salida_2, lambda: self._handle_salida_tren(datos_salida_2), prioridad=1)
            )
            print(f"Tren EMU programado para {t_salida_2.time()}")

        t_demanda = self.fecha_actual + dt.timedelta(minutes=2)
        datos_demanda = {'estacion_id': 'todas'}

        self.linea_eventos.insertar_evento_futuro(
            Evento(TipoEvento.GENERAR_DEMANDA, t_demanda, lambda: self._handle_generar_demanda(datos_demanda), prioridad=2)
        )
        print(f"Generación de pasajeros programada.")

    def avanzar_turno(self):
        #Paso del tiempo en la simulación
        #Mira la agenda de eventos y ejecuta el de mayor prioridad
        #Adelante la simulacion hasta el siguiente evento
        #Ejecuta el evento
        self.estado_simulacion.debe_pausar = False 
        
        eventos = self.linea_eventos.obtener_proximos()
        if not eventos: return False
        nueva_fecha = self.linea_eventos.consumir_eventos(eventos)
        self.fecha_actual = nueva_fecha
        self.estado_simulacion.hora_actual = self.fecha_actual.strftime("%H:%M:%S")
        
        print(f"Hora: {self.estado_simulacion.hora_actual}")
        
        pausa = self.estado_simulacion.debe_pausar
        return pausa