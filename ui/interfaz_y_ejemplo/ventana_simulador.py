import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime, time
import random
from config.configuracion import configuracion as cfg
from logic.sistema_guardado import SistemaDeGuardado
from .ventana_cargadatos import abrir_cargadatos
from .ventana_gestion import abrir_gestion_entidades as abgsen

def abrir_simulador(ventana_main, motor_instance, estado_simulacion):

    ventana = tk.Toplevel(ventana_main)
    ventana.title("Ferrocarriles")
    ventana.geometry(cfg.size_Sim)
    ventana.grab_set() 

    topLevel = tk.Menu(ventana)
    ventana.config(menu=topLevel)

    def guardar_click():
        guardador = SistemaDeGuardado()
        guardador.guardar_simulacion(estado_simulacion, "simulacion_guardada.json")
        tk.messagebox.showinfo("Guardado", "Estado guardado en 'simulacion_guardada.json'")

    tp_archivo = tk.Menu(topLevel, tearoff=0)
    tp_archivo.add_command(label="Guardar Estado", command=guardar_click)
    tp_archivo.add_command(label="Cargar Estado", command=lambda: abrir_cargadatos(ventana))
    tp_archivo.add_separator()
    tp_archivo.add_command(label="Salir", command=ventana.destroy)
    topLevel.add_cascade(label="Archivo", menu=tp_archivo)

    tp_ver = tk.Menu(topLevel, tearoff=0)
    tp_ver.add_command(label="Indicadores (RF07)")
    tp_ver.add_command(label="Línea Temporal (RF09)")
    topLevel.add_cascade(label="Ver", menu=tp_ver)

    tp_ayuda = tk.Menu(topLevel, tearoff=0)
    tp_ayuda.add_command(label="Acerca de...")
    topLevel.add_cascade(label="Ayuda", menu=tp_ayuda)

    sidebar = tk.Frame(ventana, bg=cfg.col_Bg, width=250, relief="sunken", borderwidth=1)
    sidebar.pack(side="left", fill="y") 

    mainMap = tk.Frame(ventana, bg="White")
    mainMap.pack(side="right", expand=True, fill="both")
    tk.Label(mainMap, text="Área de Simulación (Mapa)").place(relx=0.5, rely=0.5, anchor="center")

    frame_info = tk.LabelFrame(sidebar, text="Estado del Sistema", bg=cfg.col_Bg, font=("Arial", 10, "bold"))
    frame_info.pack(padx=10, pady=10, fill="x")

    lbl_hora = tk.Label(frame_info, text=f"Hora: {estado_simulacion.hora_actual}", font=cfg.font_Hora, bg=cfg.col_Bg, anchor="w")
    lbl_hora.pack(fill="x", padx=5, pady=2)

    lbl_fecha = tk.Label(frame_info, text="Fecha: 01/03/2015", font=("Arial", 10), bg=cfg.col_Bg, anchor="w")
    lbl_fecha.pack(fill="x", padx=5, pady=2)

    lbl_status = tk.Label(frame_info, text="Estado: EN ESPERA", font=("Arial", 10), fg="orange", bg=cfg.col_Bg, anchor="w")
    lbl_status.pack(fill="x", padx=5, pady=2)

    frame_ind = tk.LabelFrame(sidebar, text="Indicadores (RF07)", bg=cfg.col_Bg, font=("Arial", 10, "bold"))
    frame_ind.pack(fill="x", padx=10, pady=20) 

    tk.Label(frame_ind, text="Congestión de Vías:", bg=cfg.col_Bg, font=cfg.font_Label).pack(anchor="w", padx=5, pady=(5,0))
    
    style = ttk.Style()
    style.theme_use('default') 
    style.configure("Verde.Horizontal.TProgressbar", background=cfg.col_Success)
    style.configure("Amarillo.Horizontal.TProgressbar", background=cfg.col_Warning)
    style.configure("Rojo.Horizontal.TProgressbar", background=cfg.col_Danger)

    frame_barra = tk.Frame(frame_ind, bg=cfg.col_Bg)
    frame_barra.pack(fill="x", padx=5, pady=5)

    barra_congestion = ttk.Progressbar(frame_barra, orient="horizontal", length=100, mode="determinate")
    barra_congestion.pack(side="left", fill="x", expand=True)
    
    lbl_porcentaje = tk.Label(frame_barra, text="0%", bg=cfg.col_Bg, font=("Arial", 9, "bold"), width=5, anchor="e")
    lbl_porcentaje.pack(side="right", padx=5)

    tk.Frame(frame_ind, height=1, bg="#bdc3c7").pack(fill="x", pady=5) 
    
    tk.Label(frame_ind, text="Estación Crítica:", bg=cfg.col_Bg, font=cfg.font_Label).pack(anchor="w", padx=5)
    lbl_hotspot = tk.Label(frame_ind, text="[Calculando...]", bg=cfg.col_Bg, fg=cfg.col_Text_Sec, font=("Arial", 10, "italic"))
    lbl_hotspot.pack(anchor="w", padx=15, pady=(0, 10))

    def actualizar_indicadores(valor_decimal, nombre_estacion_critica="[Ninguna]"):
        porcentaje = int(valor_decimal * 100)
        barra_congestion['value'] = porcentaje
        lbl_porcentaje.config(text=f"{porcentaje}%") 
        lbl_hotspot.config(text=nombre_estacion_critica) 

        if porcentaje < 50:
            barra_congestion.configure(style="Verde.Horizontal.TProgressbar")
            lbl_porcentaje.config(fg=cfg.col_Success)
        elif 50 <= porcentaje < 80:
            barra_congestion.configure(style="Amarillo.Horizontal.TProgressbar")
            lbl_porcentaje.config(fg=cfg.col_Warning)
        else:
            barra_congestion.configure(style="Rojo.Horizontal.TProgressbar")
            lbl_porcentaje.config(fg=cfg.col_Danger)

    def ejecutar_avance():
        debe_pausar = motor_instance.avanzar_turno()
        lbl_hora.config(text=f"Hora: {estado_simulacion.hora_actual}")

        ocupacion_simulada = random.uniform(0.3, 0.9) 
        estaciones_simuladas = ["Est. Central", "Rancagua", "Talca", "Chillán"]
        hotspot_simulado = random.choice(estaciones_simuladas)
        actualizar_indicadores(ocupacion_simulada, hotspot_simulado)
        
        if debe_pausar:
            lbl_status.config(text="Estado: EVENTO TREN", fg="blue")
        else:
            lbl_status.config(text="Estado: EN EJECUCIÓN", fg="green")

    btn_avanzar = tk.Button(
        sidebar,
        text="Avanzar Turno",
        font=cfg.font_Avanzar,
        bg=cfg.col_Avanzar,
        cursor="hand2",
        activebackground=cfg.col_Avanzar_Hover,
        fg="black",
        command=ejecutar_avance
    )
    btn_avanzar.pack(padx=10, pady=10, fill="x") 
    
    btn_timeline = tk.Button(sidebar, text="Ver Línea Temporal", font=cfg.font_Avanzar, bg="#e1e1e1", cursor="hand2")
    btn_timeline.pack(padx=10, pady=5, fill="x")

    frame_gestion = tk.LabelFrame(sidebar, text="Gestión de Datos", bg=cfg.col_Bg, font=("Arial", 10, "bold"))
    frame_gestion.pack(fill="x", padx=10, pady=10)

    tk.Button(frame_gestion, text="Gestionar Estaciones", command=lambda: abgsen(ventana, 0)).pack(fill="x", padx=5, pady=2)
    tk.Button(frame_gestion, text="Gestionar Trenes", command=lambda: abgsen(ventana, 1)).pack(fill="x", padx=5, pady=2)
    tk.Button(frame_gestion, text="Gestionar Rutas", command=lambda: abgsen(ventana, 2)).pack(fill="x", padx=5, pady=2)