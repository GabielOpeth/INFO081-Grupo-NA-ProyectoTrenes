import datetime as dt

#Algunas clases internas de eventos
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
        
#A continuacion se muestra la clase de la linea principal de eventos
class LineaDeEventosSimple:

    def __init__(self, fecha_inicio):
        self.cola_eventos = []
        self.fecha_actual = fecha_inicio

    def insertar_evento_futuro(self, evento):
        #Se agrega el evento a la lista
        self.cola_eventos.append(evento)
        #Se ordena la lista
        self.cola_eventos.sort()

    def obtener_proximos(self, eliminar=True):
        if not self.cola_eventos:
            return []
            
        #El evento màs cercano esta en el indice 0
        hora_proxima = self.cola_eventos[0].ocurrencia
        
        procesar = []
        eventos_futuros = []
        
        #Iteracion para filtrar los eventos por coincidencia de hora
        for evento in self.cola_eventos:
            if evento.ocurrencia == hora_proxima:
                procesar.append(evento)
            else:
                #Va a la lista de futuros si la hora es diferente
                eventos_futuros.append(evento)
                
        if eliminar:
            #Se reemplaza con los eventos que no se usaron
            self.cola_eventos = eventos_futuros
            
        return procesar
        
    def consumir_eventos(self, eventos, historial=True):
        if eventos: self.fecha_actual = eventos[0].ocurrencia
        return self.fecha_actual

#Clase del motor principal del proyecto
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
        print("Iniciando Simulación...")
        
        #A continuacion, todo lo que sigue sirve para iniciar con los datos cargados del anexo. PD: tal vez despues quito esto, estamos probando que funcione

        #1: Tren 1 BMU de Ida, del anexo
        tren_bmu = self.gestor_entidades.obtener_tren("Tren BMU")
        ruta_ida = self.gestor_entidades.gestor_rutas.consultar(1) #Santiago a Rancagua
        
        if tren_bmu and ruta_ida:
            t_salida = self.fecha_actual + dt.timedelta(minutes=5)
            self.linea_eventos.insertar_evento_futuro(Evento(t_salida, "SALIDA_TREN", 
                {'tren_id': tren_bmu.id, 'ruta': ruta_ida, 'estacion_origen_id': ruta_ida.origen.id}))
            print(f"✅ Tren BMU programado para {t_salida.time()}")

        #2: tren 2 EMU de Vuelta
        tren_emu = self.gestor_entidades.obtener_tren("Tren EMU")
        ruta_vuelta = self.gestor_entidades.gestor_rutas.consultar(2) #Rancagua a Santiago
        
        if tren_emu and ruta_vuelta:
            t_salida_2 = self.fecha_actual + dt.timedelta(minutes=20) #Sale 20 minutos despues
            self.linea_eventos.insertar_evento_futuro(Evento(t_salida_2, "SALIDA_TREN", 
                {'tren_id': tren_emu.id, 'ruta': ruta_vuelta, 'estacion_origen_id': ruta_vuelta.origen.id}))
            print(f"✅ Tren EMU programado para {t_salida_2.time()}")

        #Generacion de demanda
        t_demanda = self.fecha_actual + dt.timedelta(minutes=2)
        self.linea_eventos.insertar_evento_futuro(Evento(t_demanda, "GENERAR_DEMANDA", 
            {'estacion_id': 'todas'}, prioridad=2))
        print(f"✅ Generación de pasajeros programada.")

    #Esta funcion ejecuta un a logica de simulacpon por turnos
    def avanzar_turno(self):
        eventos = self.linea_eventos.obtener_proximos() #Obtiene los eventos
        if not eventos: return False    #Si esta vacio, detiene

        #Actualiza la fecha acual a la hora del evento  
        nueva_fecha = self.linea_eventos.consumir_eventos(eventos)
        self.fecha_actual = nueva_fecha
        self.estado_simulacion.hora_actual = self.fecha_actual.strftime("%H:%M:%S") #Sincroniza la hora con estado_simulacion.py
        
        print(f"Hora: {self.estado_simulacion.hora_actual}")
        pausa = False

        #Logica: loop principal
        for ev in eventos:
            #Se activa para obtener la pausa del interfaz
            if ev.tipo in [1, 2]: pausa = True 

            #Logica de la generacion de demanda
            if ev.nombre == "GENERAR_DEMANDA":
                #Crea a las personas esperando en estaciones
                self.gestor_entidades.generar_demanda(ev.datos['estacion_id'])
                #Se programa el proximo evento de generacion de demanda
                prox = self.fecha_actual + dt.timedelta(minutes=15)
                self.linea_eventos.insertar_evento_futuro(Evento(prox, "GENERAR_DEMANDA", ev.datos))

            #Logica de salida del tren
            elif ev.nombre == "SALIDA_TREN":
                tren = self.gestor_entidades.obtener_tren(ev.datos['tren_id'])
                ruta = ev.datos['ruta']
                #Actualiza el estado del tren a 'ruta'
                self.gestor_entidades.mover_tren_a_ruta(tren, ruta)
                #Calcula la hora de llegada
                llegada = self.fecha_actual + self._calcular_tiempo_viaje(tren, ruta)
                #Establece el evento futuro de llegada a estacion
                self.linea_eventos.insertar_evento_futuro(Evento(llegada, "LLEGADA_TREN", 
                    {'tren_id': tren.id, 'estacion_destino_id': ruta.destino.id, 'ruta': ruta}))
            
            #Lofica de la llegada del tren
            elif ev.nombre == "LLEGADA_TREN":
                tren = self.gestor_entidades.obtener_tren(ev.datos['tren_id'])
                est = self.gestor_entidades.obtener_estacion(ev.datos['estacion_destino_id'])
                #Procesa la llegada del tren
                self.gestor_entidades.procesar_llegada_tren(tren, est)
                #Programa la proxima salida
                salida = self.fecha_actual + dt.timedelta(minutes=10) #Establecida por 10 minutos de espera
                #Determina la proxima ruta a tomar por el tren
                prox_ruta = self.gestor_entidades.obtener_proxima_ruta(est, tren)
                #Programa la nueva salida (es decir, la salida en si, no la proxima) del tren
                self.linea_eventos.insertar_evento_futuro(Evento(salida, "SALIDA_TREN", 
                    {'tren_id': tren.id, 'ruta': prox_ruta, 'estacion_origen_id': est.id}))

        return pausa