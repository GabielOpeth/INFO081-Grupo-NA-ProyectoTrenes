class MotorSimulacion:
    def __init__(self, gestor_entidades, estado_simulacion):
        # ... (tus importaciones y atributos ya existentes) ...
        
        self.gestor_entidades = gestor_entidades
        self.estado_simulacion = estado_simulacion

        # --- Lógica de Inicialización Segura de Fecha ---
        
        # Hora por defecto según el estándar de inicio de simulación.
        HORA_INICIAL_DEFAULT = "07:00:00"
        FECHA_BASE = "01-03-2015" # Fecha fija para el RF04
        FORMATO = "%d-%m-%Y %H:%M:%S"

        # 1. Obtener la hora del estado, usando el valor por defecto si es None o inválida
        hora_str = getattr(self.estado_simulacion, 'hora_actual', HORA_INICIAL_DEFAULT)
        
        # Si por alguna razón la hora es None o vacía, usamos el default.
        if not hora_str:
            hora_str = HORA_INICIAL_DEFAULT

        # 2. Construir la cadena completa
        fecha_base_str = f"{FECHA_BASE} {hora_str}"
        
        # 3. Intentar parsear (conversión)
        try:
            # Crea el objeto datetime. (Asumimos que esta era la línea 38 que daba error)
            fecha_inicial_dt = dt.datetime.strptime(fecha_base_str, FORMATO)
        except (ValueError, TypeError) as e:
            # Esto captura el error si la cadena resultante no coincide con el formato.
            print(f"Advertencia: Error de formato ('{e}') al iniciar la hora ('{fecha_base_str}'). Usando 07:00:00 por defecto.")
            fecha_inicial_dt = dt.datetime(2015, 3, 1, 7, 0, 0)
        
        # 4. Inicializar el motor de eventos (RF03)
        try:
            from eventos_admin.linea_de_eventos import LineaDeEventos
        except ImportError:
            # Aquí maneja si falla la importación, no debe continuar sin el módulo.
            print("ERROR: No se pudo importar LineaDeEventos. Revisa el submódulo.")
            return # o raise error
            
        self.linea_eventos = LineaDeEventos(self.estado_simulacion, fecha_inicial_dt)
        self.fecha_actual = fecha_inicial_dt