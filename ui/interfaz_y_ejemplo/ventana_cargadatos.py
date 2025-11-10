import tkinter as tk
from config import configuracion as cfg
from tkinter import messagebox
from logic.sistema_guardado import SistemaDeGuardado

def abrir_cargadatos(ventana_main):

    # dev msg: cambiamos por Toplevel
    carga_pantalla = tk.Toplevel(ventana_main)
    carga_pantalla.title("CARGAR DATOS")
    carga_pantalla.geometry(cfg.size_Load)
    
    # freeze
    carga_pantalla.grab_set()

    # dev msg: codigo original
    tk.Label(carga_pantalla, text="Ingresa el nombre del archivo guardado (con o sin .json):",
             font=cfg.font_Label).pack(pady=10)
             
    entrada = tk.Entry(carga_pantalla, font=cfg.font_Label)
    entrada.pack(padx=20, pady=10, fill="x", expand=True)

    #cargar archivo--------------------------------
    def ejecutar_carga():
        """
        Función interna que se llama al presionar el botón Cargar.
        """
        # Obtiene el texto del campo 'entrada'
        nombre_archivo = entrada.get()
        
        # Validación simple
        if not nombre_archivo:
            messagebox.showwarning("Campo Vacío", "Por favor, ingresa un nombre de archivo.")
            return # No continúa si no hay texto

        # Asegura que el archivo termine en .json
        if not nombre_archivo.endswith(".json"):
            nombre_archivo += ".json"
            
        try:
            # Intenta cargar los datos usando tu clase
            cargador = SistemaDeGuardado()
            datos = cargador.cargar_simulacion(nombre_archivo)
            
            # Muestra un mensaje de éxito
            messagebox.showinfo("Éxito", f"Simulación '{nombre_archivo}' cargada correctamente.\nHora guardada: {datos.get('hora_actual')}")
            
            # Cierra la ventana de carga si todo salió bien
            carga_pantalla.destroy() 
            
        except FileNotFoundError:
            # Error si el archivo no existe
            messagebox.showerror("Error", f"No se pudo encontrar el archivo: {nombre_archivo}")
        except Exception as e:
            # Error para cualquier otro problema
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    # --- PASO 3: Añade el botón de confirmación ---
    
    btn_confirmar = tk.Button(
        carga_pantalla,
        text="Cargar Simulación",
        font=cfg.font_Boton,  # Usa la fuente de tu configuración
        command=ejecutar_carga # Llama a la función que creamos
    )
    btn_confirmar.pack(pady=10, padx=20, fill="x")