# motor_simulacion.py

import sys
import os
import datetime as dt

# =======================================================
# 1. Ajuste de Path e Importación del Submódulo (eventos_admin)
# =======================================================

# Ajustar la ruta para encontrar los módulos en la raíz del proyecto
# Esto es necesario si 'eventos_admin' está en la raíz y no en 'logic'.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Dependencias del Submódulo ---
try:
    # Asumimos que estas clases están en el submódulo 'eventos_admin'
    from eventos_admin.linea_de_eventos import LineaDeEventos 
    from eventos_admin.eventos import Evento, TipoEvento
    
except ImportError as e:
    print(f"ERROR CRÍTICO: No se pudo importar un componente de 'eventos_admin'. Asegúrate de que los submódulos estén inicializados. Detalle: {e}")
    # Definimos clases dummy para evitar un crash, pero la simulación no funcionará sin el submódulo
    class LineaDeEventos:
        def __init__(self, *args, **kwargs): pass
        def obtener_proximos(self, eliminar=True): return []
        def consumir_eventos(self, eventos, historial=True): return dt.datetime.now()
        def insertar_evento_futuro(self, evento): pass
    class Evento:
        def __init__(self, *args, **kwargs): pass
    class TipoEvento:
        SALIDA_TREN = 1
        LLEGADA_TREN = 2
        GENERAR_DEMANDA = 3


class MotorSimulacion:
    
    def __init__(self, gestor_entidades, estado_simulacion):
        
        self.gestor_entidades = gestor_entidades
        self.estado_simulacion = estado_simulacion

        # --- Inicialización Segura de Fecha ---
        HORA_INICIAL_DEFAULT = "07:00:00"
        FECHA_BASE = "01-03-2015" # Fecha del RF04
        FORMATO = "%d-%m-%Y %H:%M:%S"

        hora_str = getattr(self.estado_simulacion, 'hora_actual', HORA_INICIAL_DEFAULT)
        if not hora_str: hora_str = HORA_INICIAL_DEFAULT

        fecha_base_str = f"{FECHA_BASE} {hora_str}"
        
        try:
            fecha_inicial_dt = dt.datetime.strptime(fecha_base_str, FORMATO)
        except (ValueError, TypeError):
            fecha_inicial_dt = dt.datetime(2015, 3, 1, 7, 0, 0)
        
        # Inicializa la línea de eventos (RF03)
        self.linea_eventos = LineaDeEventos(self.estado_simulacion, fecha_inicial_dt)
        self.fecha_actual = fecha_inicial_dt
        
        print(f"Motor Inicializado. Hora de inicio: {self.fecha_actual.strftime(FORMATO)}")

    # =======================================================
    # 2. LÓGICA AUXILIAR
    # =======================================================

    def _calcular_tiempo_viaje(self, tren, ruta) -> dt.timedelta:
        """Calcula el tiempo de viaje basado en Ruta y Tren."""
        # Tiempo (horas) = Longitud (km) / Velocidad (km/h)
        velocidad_kmh = tren.velocidad if tren and tren.velocidad > 0 else 80 
        tiempo_horas = ruta.longitud_km / velocidad_kmh
        segundos = tiempo_horas * 3600 
        return dt.timedelta(seconds=int(segundos))

    # =======================================================
    # 3. IMPLEMENTACIÓN DE iniciar_simulacion() (RF04)
    # =======================================================

    def iniciar_simulacion(self):
        """
        Coordina la carga de datos iniciales (RF04) y programa los primeros eventos.
        """
        print("--- Carga de Entidades y Eventos Iniciales ---")
        
        # 1. Cargar Datos Iniciales (RF04)
        self.gestor_entidades.cargar_datos_iniciales_rf04()
        
        try:
            # 2. Obtener entidades iniciales (asumiendo IDs)
            tren_inicial = self.gestor_entidades.obtener_tren("Tren_BMU")
            ruta_inicial = self.gestor_entidades.obtener_ruta("Ruta_STGO_RANCAGUA")
            
            # 3. Programar Salida Inicial de Tren (RF03)
            tiempo_salida = self.fecha_actual.replace(minute=self.fecha_actual.minute + 5, second=0)
            
            primer_evento = Evento(
                ocurrencia=tiempo_salida, 
                nombre="SALIDA_TREN", 
                datos={'tren_id': tren_inicial.id, 'ruta': ruta_inicial, 'estacion_origen_id': ruta_inicial.origen.id},
                prioridad=1
            )
            self.linea_eventos.insertar_evento_futuro(primer_evento)
            print(f"✅ Programado: {primer_evento.nombre} a las {primer_evento.ocurrencia.strftime('%H:%M:%S')}")

            # 4. Programar Generación de Demanda Inicial (RF05)
            tiempo_demanda = self.fecha_actual.replace(minute=self.fecha_actual.minute + 10, second=0)
            evento_demanda = Evento(ocurrencia=tiempo_demanda, nombre="GENERAR_DEMANDA", datos={}, prioridad=5)
            self.linea_eventos.insertar_evento_futuro(evento_demanda)

        except AttributeError as e:
            print(f"⛔ ERROR: Faltan entidades iniciales para RF04. {e}. No se programaron eventos de tren.")


    # =======================================================
    # 4. IMPLEMENTACIÓN DE avanzar_turno() (RF03, RF02)
    # =======================================================
    
    def avanzar_turno(self):
        """
        Procesa el/los próximo(s) evento(s) en la cola y programa las consecuencias. (RF03)
        Retorna: True si la GUI debe pausar (evento de tren).
        """
        
        # 1. Obtener Eventos
        eventos_a_procesar = self.linea_eventos.obtener_proximos(eliminar=False)
        
        if not eventos_a_procesar:
            return False

        # 2. Consumir Eventos (Actualiza fecha, mueve al historial)
        fecha_proxima = self.linea_eventos.consumir_eventos(eventos_a_procesar, historial=True)
        self.fecha_actual = fecha_proxima
        self.estado_simulacion.hora_actual = self.fecha_actual.strftime("%H:%M:%S")
        
        debe_pausar = False
        
        # 3. Procesamiento de Lógica (Generar nuevos eventos)
        for evento in eventos_a_procesar:
            
            # Decidir si pausar (RF03)
            # Utilizamos getattr para obtener el valor de la enumeración TipoEvento.
            if getattr(evento, 'tipo', None) in [TipoEvento.LLEGADA_TREN, TipoEvento.SALIDA_TREN]: 
                debe_pausar = True

            # --- LÓGICA DE EVENTOS (Separación de Responsabilidades) ---
            
            if evento.nombre == "SALIDA_TREN":
                # RF02: Llama a la lógica de tu compañero para mover el tren y actualizar el estado
                tren = self.gestor_entidades.obtener_tren(evento.datos['tren_id'])
                ruta = evento.datos['ruta']
                
                self.gestor_entidades.mover_tren_a_ruta(tren, ruta) 
                
                # Calcular y programar llegada (Tu lógica)
                tiempo_viaje = self._calcular_tiempo_viaje(tren, ruta)
                tiempo_llegada = self.fecha_actual + tiempo_viaje
                
                evento_llegada = Evento(
                    ocurrencia=tiempo_llegada, 
                    nombre="LLEGADA_TREN", 
                    datos={'tren_id': tren.id, 'estacion_destino_id': ruta.destino.id, 'ruta': ruta}
                )
                self.linea_eventos.insertar_evento_futuro(evento_llegada)
                
            elif evento.nombre == "LLEGADA_TREN":
                # RF02: Llama a la lógica de tu compañero para procesar la llegada y el estado
                tren = self.gestor_entidades.obtener_tren(evento.datos['tren_id'])
                estacion = self.gestor_entidades.obtener_estacion(evento.datos['estacion_destino_id'])
                
                self.gestor_entidades.procesar_llegada_tren(tren, estacion) # Mueve, sube/baja pasajeros, actualiza flujo
                
                # Programar próximo evento de salida/rotación (Tu lógica)
                tiempo_salida = self.fecha_actual + dt.timedelta(minutes=5)
                proxima_ruta = self.gestor_entidades.obtener_proxima_ruta(estacion, tren) # Llama a la lógica de tu compañero
                
                evento_salida = Evento(
                    ocurrencia=tiempo_salida, 
                    nombre="SALIDA_TREN", 
                    datos={'tren_id': tren.id, 'ruta': proxima_ruta, 'estacion_origen_id': estacion.id}
                )
                self.linea_eventos.insertar_evento_futuro(evento_salida)
                
            elif evento.nombre == "GENERAR_DEMANDA":
                # Lógica del compañero de RF05
                self.gestor_entidades.generar_demanda(evento.datos['estacion_id'])
                
                # Programar el próximo evento de generación de demanda
                tiempo_proxima_demanda = self.fecha_actual + dt.timedelta(minutes=15)
                proximo_evento_demanda = Evento(ocurrencia=tiempo_proxima_demanda, nombre="GENERAR_DEMANDA", datos={'estacion_id': 'todas'}, prioridad=5)
                self.linea_eventos.insertar_evento_futuro(proximo_evento_demanda)
            
        # 4. Devolver instrucción a la GUI (RF03)
        return debe_pausar