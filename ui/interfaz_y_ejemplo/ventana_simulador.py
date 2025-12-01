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
from config.configuracion import configuracion as cfg
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

    sidebar = tk.Frame(ventana,
                       bg=cfg.col_Bg,
                       width=250,
                       relief="sunken",
                       borderwidth=1)
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
    frame_info = tk.LabelFrame(sidebar, text="Estado del Sistema",
                               bg=cfg.col_Bg,
                               font=("Arial", 10, "bold"))
    frame_info.pack(padx=10, pady=10, fill="x")

    #----- Datos en "frame_info" -----

    lbl_hora = tk.Label(frame_info,
                        text=f"Hora: {hora_actual_str}",
                        font=cfg.font_Hora,
                        bg=cfg.col_Bg,
                        anchor="w")
    lbl_hora.pack(fill="x", padx=5, pady=2)

    lbl_fecha = tk.Label(frame_info,
                         text=f"Fecha: {fecha_actual_str}",
                         font=("Arial", 10),
                         bg=cfg.col_Bg,
                         anchor="w")
    lbl_fecha.pack(fill="x", padx=5, pady=2)

    lbl_status = tk.Label(frame_info,
                          text="Estado: PAUSADO",
                          font=("Arial", 10),
                          fg="red",
                          bg=cfg.col_Bg, 
                          anchor="w") #dev note: Cambiar texto fijo por string del estado de simulación en el producto final
    lbl_status.pack(fill="x", padx=5, pady=2)

    #----- Botones laterales -----

    # Siguiente estado

    btn_avanzar = tk.Button(
        sidebar,
        text="Avanzar Turno",
        font=cfg.font_Avanzar,
        bg=cfg.col_Avanzar,
        cursor="hand2",
        activebackground=cfg.col_Avanzar_Hover,
        fg="black",
    )
    btn_avanzar.pack(padx=10, pady=10, fill="x") # fill="x" hace que ocupe el ancho del panel
    
    # Línea Temporal
    btn_timeline = tk.Button(sidebar,
                             text="Ver Línea Temporal",
                             font=cfg.font_Avanzar,
                             bg="#e1e1e1",
                             cursor="hand2")
    btn_timeline.pack(padx=10, pady=5, fill="x")

    # =========================================================
    # 2. PANEL DE INDICADORES (RF07)
    # =========================================================
    
    # A. Configuración de Estilos (Semáforo)
    # Definimos 3 "clases" visuales para la barra según la gravedad
    style = ttk.Style()
    style.theme_use('default') # Usamos 'default' para facilitar el cambio de colores
    style.configure("Verde.Horizontal.TProgressbar", background=cfg.col_Success)
    style.configure("Amarillo.Horizontal.TProgressbar", background=cfg.col_Warning)
    style.configure("Rojo.Horizontal.TProgressbar", background=cfg.col_Danger)

    # B. Marco del Panel
    frame_ind = tk.LabelFrame(sidebar,
                            text="Indicadores (RF07)", 
                            bg=cfg.col_Bg,
                            font=("Arial", 10, "bold"))
    frame_ind.pack(fill="x", padx=10, pady=20) 

    # --- INDICADOR 1: CONGESTIÓN DE VÍAS ---
    tk.Label(frame_ind, text="Congestión de Vías:", 
             bg=cfg.col_Bg,
             font=cfg.font_Label).pack(anchor="w", padx=5, pady=(5,0))
    
    # Contenedor auxiliar para poner la Barra y el Texto % juntos
    frame_barra = tk.Frame(frame_ind,
                           bg=cfg.col_Bg)
    frame_barra.pack(fill="x", padx=5, pady=5)

    # 1. La Barra (Widget)
    # length=100 es el tamaño visual en pixeles
    barra_congestion = ttk.Progressbar(frame_barra,
                                    orient="horizontal",
                                    length=100,
                                    mode="determinate",)
    barra_congestion.pack(side="left", fill="x", expand=True)
    
    # 2. El Texto del Porcentaje
    lbl_porcentaje = tk.Label(frame_barra,
                                text="0%",
                                bg=cfg.col_Bg,
                                font=("Arial", 9, "bold"),
                                width=5,
                                anchor="e")
    lbl_porcentaje.pack(side="right", padx=5)


    # --- INDICADOR 2: ESTACIÓN CRÍTICA (Hotspot) ---
    tk.Frame(frame_ind,
             height=1,
             bg="#bdc3c7").pack(fill="x", pady=5) # Separador visual
    
    tk.Label(frame_ind,
             text="Estación Crítica:", 
             bg=cfg.col_Bg,
             font=cfg.font_Label).pack(anchor="w", padx=5)
    
    lbl_hotspot = tk.Label(frame_ind,
                           text="[Ninguna]", 
                           bg=cfg.col_Bg,
                           fg=cfg.col_Text_Sec,
                           font=("Arial", 10, "italic"))
    lbl_hotspot.pack(anchor="w", padx=15, pady=(0, 10))

# =========================================================
    # 3. LÓGICA DE INTERFAZ (Motor Visual)
    # =========================================================
    # Esta función es la que usarán tus compañeros. 
    # Ellos te envían un float (0.85) y tú haces la magia visual.
    
    def actualizar_indicadores(valor_decimal, nombre_estacion_critica="[Ninguna]"):
        """
        Input: 
            valor_decimal (float): Un número entre 0.0 y 1.0
            nombre_estacion_critica (str): Nombre de la estación con más gente
        """
        # 1. Matemáticas: Convertir 0.0-1.0 a 0-100
        porcentaje = int(valor_decimal * 100)
        
        # 2. Actualizar Widgets
        barra_congestion['value'] = porcentaje      # Mueve la barra
        lbl_porcentaje.config(text=f"{porcentaje}%") # Actualiza el texto numérico
        lbl_hotspot.config(text=nombre_estacion_critica) # Actualiza el hotspot

        # 3. Lógica de Semáforo (Cambio de color)
        if porcentaje < 50:
            barra_congestion.configure(style="Verde.Horizontal.TProgressbar")
            lbl_porcentaje.config(fg=cfg.col_Success)
        elif 50 <= porcentaje < 80:
            barra_congestion.configure(style="Amarillo.Horizontal.TProgressbar")
            lbl_porcentaje.config(fg=cfg.col_Warning)
        else: # Mayor a 80% (Crítico)
            barra_congestion.configure(style="Rojo.Horizontal.TProgressbar")
            lbl_porcentaje.config(fg=cfg.col_Danger)


    # =========================================================
    # 4. HERRAMIENTA DE DESARROLLO (DEV TOOL)
    # =========================================================
    # ESTO ES TEMPORAL. Te permite probar la barra moviendo un slider.
    # Bórralo cuando conectes el código final.
    
    lbl_dev = tk.Label(mainMap,
                       text="[DEV TOOL] Prueba Visual Indicadores:",
                       bg="white",
                       fg="blue")
    lbl_dev.place(relx=0.5, rely=0.85, anchor="center")

    def prueba_slider(valor):
        v = float(valor)
        # Inventamos nombres de estación según la gravedad para probar
        est = "Est. Central" if v > 0.8 else "Est. Los Lagos" if v > 0.4 else "[Ninguna]"
        actualizar_indicadores(v, est)

    slider_dev = tk.Scale(mainMap, from_=0.0, to=1.0, resolution=0.01, orient="horizontal", length=200, command=prueba_slider)
    slider_dev.place(relx=0.5, rely=0.90, anchor="center")

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