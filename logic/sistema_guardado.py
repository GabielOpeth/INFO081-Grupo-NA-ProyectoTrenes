# En logic/sistema_guardado.py

import json             #Requerido para el sistema de guardado, usa formato .json
import datetime as dt   #Uso de las fechas.
# Importamos todas las clases necesarias para reconstruir los objetos
from .estado_simulacion import EstadoSimulacion #Importa el estado de simulacion para el uso del sistema de guardado
from models.estacion import Estacion    #importa los modelos correspondientes a la carpeta models
from models.tren import Tren            # ""
from models.ruta import Ruta            # ""
from models.persona import Persona      # ""


class SistemaDeGuardado:

    def guardar_simulacion(self, estado_simulacion, nombre_archivo=None):
        #Informacion a guardar de la simulacion, en un archivo json.
        data_a_guardar = estado_simulacion.to_serializable()

        if not nombre_archivo.endswith(".json"):
            nombre_archivo += ".json"

        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(data_a_guardar, archivo, indent=4, default=str) 
        
        print(f"✅ Datos guardados exitosamente en {nombre_archivo}")
    
    """
    Toda esta seccion sirve como base de la logica para cargar una simulacion ya guardada 
    """
    def cargar_simulacion(self, nombre_archivo=None):

        #Intento de uso de archivos (Como en la clase 1 de la unidad 2, màs o menos)
        if not nombre_archivo.endswith(".json"):
            nombre_archivo += ".json"
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                datos_cargados = json.load(archivo)
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo '{nombre_archivo}' no encontrado.")   #Evita que el programa caiga al no hallar archivo
            
        print(f"📂 Archivo leído. Iniciando reconstrucción del estado...")
        
        #Declaracion de un nuevo estado, que, basicamente, sea la reconstruccion de lo guardado en el json
        nuevo_estado = self.reconstruccion_del_guardado_json(datos_cargados)
        
        print(f"✅ Estado reconstruido exitosamente. Hora: {nuevo_estado.hora_actual}")
        return nuevo_estado

    #Directamente relacionada al Sistema de Guardado, recoge los datos del json basicamente
    def reconstruccion_del_guardado_json(self, data):
        nuevo_estado = EstadoSimulacion()
        nuevo_estado.hora_actual = data.get("hora_actual", "07:00:00")
  
        gestor = nuevo_estado.gestor_entidades
        
        #Una limpieza necesaria para los gestores .clear()
        gestor.gestor_estaciones.estaciones.clear()
        gestor.gestor_trenes.trenes.clear()
        gestor.gestor_rutas.rutas.clear()
        gestor.gestor_personas.personas.clear()

        entidades_data = data.get('entidades', {})
        
        #Logica de la reconstruccion (mayorente en base al recorrido de los datos del mismo archivo json)

        #1ro, la reconstruccion de las estaciones
        for est_data in entidades_data.get('estaciones', []):
            nueva_estacion = Estacion(
                est_data['id'], est_data['nombre'], est_data['poblacion'], est_data['vias']
            )
            nueva_estacion.flujo_acumulado = est_data.get('flujo_acumulado', 0)
            nueva_estacion.pasajeros_esperando = est_data.get('pasajeros_esperando', 0)
            gestor.gestor_estaciones.estaciones[nueva_estacion.id] = nueva_estacion
            
            if nueva_estacion.id >= gestor.gestor_estaciones.next_id:
                gestor.gestor_estaciones.next_id = nueva_estacion.id + 1

        #2do, reconstruccion de trenes
        for tren_data in entidades_data.get('trenes', []):
            nuevo_tren = Tren(
                tren_data['id'], tren_data['velocidad'], tren_data['nombre'], tren_data['vagones']
            )
            gestor.gestor_trenes.trenes[nuevo_tren.id] = nuevo_tren
            
            if nuevo_tren.id >= gestor.gestor_trenes.next_id:
                gestor.gestor_trenes.next_id = nuevo_tren.id + 1

        #3ro, reconstruir las rutas (depende de la estacion )
        for ruta_data in entidades_data.get('rutas', []):
            origen_id = ruta_data['origen_id']
            destino_id = ruta_data['destino_id']
            obj_origen = gestor.gestor_estaciones.consultar(origen_id)
            obj_destino = gestor.gestor_estaciones.consultar(destino_id)
            
            if obj_origen and obj_destino:
                nueva_ruta = Ruta(
                    ruta_data['id'], obj_origen, obj_destino, ruta_data['longitud_km']
                )
                gestor.gestor_rutas.rutas[nueva_ruta.id] = nueva_ruta
                
                if nueva_ruta.id >= gestor.gestor_rutas.next_id:
                    gestor.gestor_rutas.next_id = nueva_ruta.id + 1

        #4to, reconstruir a las personas
        for p_data in entidades_data.get('personas', []):
            try:
                # Conversión de string ISO a objeto datetime (Visto en clases)
                tiempo_dt = dt.datetime.fromisoformat(p_data['tiempo_llegada'])
            except ValueError:
                tiempo_dt = dt.datetime.now() 

            nueva_persona = Persona(
                p_data['id'], p_data['origen_id'], p_data['destino_id'], tiempo_dt 
            )
            nueva_persona.viajando = p_data.get('viajando', False)
            nueva_persona.en_estacion = p_data.get('en_estacion', True)
            gestor.gestor_personas.personas[nueva_persona.id] = nueva_persona
            
            if nueva_persona.id >= gestor.gestor_personas.next_id:
                gestor.gestor_personas.next_id = nueva_persona.id + 1
            
        return nuevo_estado #termina por devolver el nuevo estado, wuju!