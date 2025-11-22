def notas(): # Notas sobre variables de referencia del archivo configuración.py, no llamar función, plegar por favor
    # /////-----///// Zona de referencia para configuración \\\\\-----\\\\\
    """
    # === Colores (hex) ===
    col_Bg = "White"
    col_Boton1 = "#002afe"  # Turquesa=#7fffd4
    col_Boton2 = "Black"
    col_Defaul = "Black"

    # === Fuentes (tuple) ===
    # (Se definen como tuplas: (Familia, Tamaño, Estilo))
    font_Titulo = ("arial", 20, "bold")
    font_Boton = ("Arial", 12)
    font_Hora = ("Arial", 10)
    font_Avanzar = ("arial", 8)
    font_Label = ("Arial", 12)

    # === Tamaños (pix) ===
    # (Tamaños de ventana en "Ancho x Alto")
    size_Start = "800x350"
    size_Sim = "1024x768"
    size_Load = "400x150"

    # (Tamaños de widgets)
    size_BotonST = 50
    size_BotonH = 1
    Tab_width = 1000  # Ancho del frame de la pestaña
    Tab_height = 1000 # Alto del frame de la pestaña
    """
    return

import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime, time
from config import configuracion as cfg
#ventanas; carga
from .ventana_cargadatos import abrir_cargadatos

def abrir_simulador (ventana_main):

    #dev msg: usamos Toplevel
    ventana = tk.Toplevel(ventana_main)
    ventana.title("Ferrocarriles")
    ventana.geometry(cfg.size_Sim)

    #freeze
    ventana.grab_set() 

    #----- Barra superior (dropdown menu)----

    topLevel = tk.Menu(ventana)
    ventana.config(menu=topLevel)

    #----- Para topLevel: Archivo -----

    tp_archivo = tk.Menu(topLevel, tearoff=0)
    tp_archivo.add_command(label="Guardar Estado") # RF08
    tp_archivo.add_command(
        label="Cargar Estado",
        command=lambda: abrir_cargadatos(ventana))  # RF08
    tp_archivo.add_separator()
    tp_archivo.add_command(label="Salir", command=ventana.destroy)
    topLevel.add_cascade(label="Archivo", menu=tp_archivo)

    #----- Para topLevel: Ver ------

    tp_ver = tk.Menu(topLevel, tearoff=0)
    tp_ver.add_command(label="Indicadores (RF07)")
    tp_ver.add_command(label="Línea Temporal (RF09)")
    topLevel.add_cascade(label="Ver", menu=tp_ver)

    #----- Para topLevel: Ayuda

    tp_ayuda = tk.Menu(topLevel, tearoff=0)
    tp_ayuda.add_command(label="Acerca de...")
    topLevel.add_cascade(label="Ayuda", menu=tp_ayuda)

    # /////-----///// Código principal \\\\\-----\\\\\ #

    #----- Barra lateral -----

    sidebar = tk.Frame(ventana, bg=cfg.col_Bg, width=250, relief="sunken", borderwidth=1)
    sidebar.pack(side="left", fill="y") # Se ancla a la izquierda y llena verticalmente

    # ----- Área simulación -----

    mainMap = tk.Frame(ventana, bg="White")
    mainMap.pack(side="right", expand=True, fill="both")

    tk.Label(mainMap, text="Área de Simulación").place(relx=0.5, rely=0.5, anchor="center") #mensaje del área de simulación

    #----- Hora y fecha -----
    hora_actual_str = datetime.now().strftime("%H:%M:%S")
    fecha_actual_str = datetime.now().strftime("%d/%m/%Y")

    #----- Información en forma de strings -----
        #dev note: Usar labels en lugar de botones
    frame_info = tk.LabelFrame(sidebar, text="Estado del Sistema", bg=cfg.col_Bg, font=("Arial", 10, "bold"))
    frame_info.pack(padx=10, pady=10, fill="x")

    #----- Datos en "frame_info" -----

    lbl_hora = tk.Label(frame_info, text=f"Hora: {hora_actual_str}", font=cfg.font_Hora, bg=cfg.col_Bg, anchor="w")
    lbl_hora.pack(fill="x", padx=5, pady=2)

    lbl_fecha = tk.Label(frame_info, text=f"Fecha: {fecha_actual_str}", font=("Arial", 10), bg=cfg.col_Bg, anchor="w")
    lbl_fecha.pack(fill="x", padx=5, pady=2)

    lbl_status = tk.Label(frame_info, text="Estado: PAUSADO", font=("Arial", 10), fg="red", bg=cfg.col_Bg, anchor="w") #dev note: Cambiar texto fijo por string del estado de simulación en el producto final
    lbl_status.pack(fill="x", padx=5, pady=2)

    #----- Botones laterales -----

    # Siguiente estado

    btn_avanzar = tk.Button(sidebar, text="Avanzar Turno", font=cfg.font_Avanzar, bg="#e1e1e1", cursor="hand2")
    btn_avanzar.pack(padx=10, pady=20, fill="x") # fill="x" hace que ocupe el ancho del panel
    
    # Línea Temporal
    btn_timeline = tk.Button(sidebar, text="Ver Línea Temporal", font=cfg.font_Avanzar, bg="#e1e1e1", cursor="hand2")
    btn_timeline.pack(padx=10, pady=5, fill="x")



    #dev note: codigo original
    """
    tk.Label(ventana, text="Primera prueba", padx=1000, pady=1000)

    ntb_tabulador = ttk.Notebook(ventana)

    tab1 = tk.Frame(ntb_tabulador, bg=cfg.col_Bg, width=cfg.Tab_width, height=cfg.Tab_height)
    tab2 = tk.Frame(ntb_tabulador, bg=cfg.col_Bg, width=cfg.Tab_width, height=cfg.Tab_height)

    ntb_tabulador.add(tab1, text="Simulacion")
    ntb_tabulador.add(tab2, text="Ayuda")
    ntb_tabulador.pack(expand=1, fill="both")
    
    boton1 = tk.Button(tab1, text=("HORA:", datetime.now()), width=30, height=1, font=cfg.font_Hora)
    boton1.place(x=0, y=0)
    
    boton2 = tk.Button(tab1, text="Avanzar turno", width=35, height=1, font=cfg.font_Avanzar)
    boton2.place(x=0, y=26)
    """