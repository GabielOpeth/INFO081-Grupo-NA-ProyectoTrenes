import tkinter as tk
from tkinter import ttk
from config.configuracion import configuracion as cfg

def abrir_gestion_entidades(parentW, tab_inicial=0):

    ventana = tk.Toplevel(parentW)
    ventana.title("Gestión de Datos del Sistema")
    ventana.geometry(cfg.size_Gestion) # Definido en tu config como 600x500
    ventana.grab_set()

    # --- CONTENEDOR DE PESTAÑAS (NOTEBOOK) ---
    notebook = ttk.Notebook(ventana)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # Creamos los marcos para cada pestaña
    tab_estaciones = tk.Frame(notebook, bg=cfg.col_Bg)
    tab_trenes = tk.Frame(notebook, bg=cfg.col_Bg)
    tab_rutas = tk.Frame(notebook, bg=cfg.col_Bg)

    notebook.add(tab_estaciones, text="Estaciones")
    notebook.add(tab_trenes, text="Trenes")
    notebook.add(tab_rutas, text="Rutas")

    # Seleccionamos la pestaña que pidió el usuario
    notebook.select(tab_inicial)

    # =======================================================
    # PESTAÑA 1: ESTACIONES
    # =======================================================
    # Diseño: Lista a la izquierda, Formulario a la derecha
    
    # --- Panel Izquierdo (Lista) ---
    pnl_izq_est = tk.Frame(tab_estaciones, bg=cfg.col_Bg, width=200)
    pnl_izq_est.pack(side="left", fill="y", padx=5, pady=5)
    
    tk.Label(pnl_izq_est, text="Estaciones", font=("Arial", 10, "bold"), bg=cfg.col_Bg).pack(anchor="w")
    lista_estaciones = tk.Listbox(pnl_izq_est, width=25)
    lista_estaciones.pack(expand=True, fill="both", pady=5)
    
    # --- Panel Derecho (Formulario) ---
    pnl_der_est = tk.Frame(tab_estaciones, bg=cfg.col_Bg)
    pnl_der_est.pack(side="right", expand=True, fill="both", padx=10, pady=5)

    # Campos (Basado en models/estacion.py: nombre, poblacion)
    tk.Label(pnl_der_est, text="Nombre:", bg=cfg.col_Bg).pack(anchor="w")
    entry_nombre_est = tk.Entry(pnl_der_est)
    entry_nombre_est.pack(fill="x", pady=(0, 10))

    tk.Label(pnl_der_est, text="Población:", bg=cfg.col_Bg).pack(anchor="w")
    entry_pob_est = tk.Entry(pnl_der_est)
    entry_pob_est.pack(fill="x", pady=(0, 10))

    # Botón Especial del Mockup
    btn_vias = tk.Button(pnl_der_est, text="Configurar Vías de Estación", bg="#e1e1e1")
    btn_vias.pack(fill="x", pady=(0, 10))

    # Selector de Generador (RF05)
    tk.Label(pnl_der_est, text="Generador de Demanda (RF05):", bg=cfg.col_Bg).pack(anchor="w")
    combo_demanda = ttk.Combobox(pnl_der_est, values=["Generador Base", "Hora Punta", "Fin de Semana"], state="readonly")
    combo_demanda.current(0)
    combo_demanda.pack(fill="x", pady=(0, 20))

    # Botones de Acción (Abajo)
    btn_crear_est = tk.Button(pnl_der_est, text="Crear Estación", bg=cfg.col_Avanzar, font=cfg.font_Boton)
    btn_crear_est.pack(fill="x", pady=5)
    
    btn_eliminar_est = tk.Button(pnl_der_est, text="Eliminar Estación", bg="#ffcccc")
    btn_eliminar_est.pack(fill="x", pady=5)

    btn_guardar_est = tk.Button(pnl_der_est, text="Guardar Cambios")
    btn_guardar_est.pack(fill="x", pady=5)


    # =======================================================
    # PESTAÑA 2: TRENES
    # =======================================================
    
    # --- Panel Izquierdo (Lista) ---
    pnl_izq_tren = tk.Frame(tab_trenes, bg=cfg.col_Bg, width=200)
    pnl_izq_tren.pack(side="left", fill="y", padx=5, pady=5)
    
    tk.Label(pnl_izq_tren, text="Trenes", font=("Arial", 10, "bold"), bg=cfg.col_Bg).pack(anchor="w")
    lista_trenes = tk.Listbox(pnl_izq_tren, width=25)
    lista_trenes.pack(expand=True, fill="both", pady=5)

    # --- Panel Derecho (Formulario) ---
    pnl_der_tren = tk.Frame(tab_trenes, bg=cfg.col_Bg)
    pnl_der_tren.pack(side="right", expand=True, fill="both", padx=10, pady=5)

    # Campos (Basado en models/tren.py: velocidad, nombre, vagones)
    tk.Label(pnl_der_tren, text="Nombre del Tren:", bg=cfg.col_Bg).pack(anchor="w")
    entry_nom_tren = tk.Entry(pnl_der_tren)
    entry_nom_tren.pack(fill="x", pady=(0, 10))

    tk.Label(pnl_der_tren, text="Velocidad (km/h):", bg=cfg.col_Bg).pack(anchor="w")
    entry_vel_tren = tk.Entry(pnl_der_tren)
    entry_vel_tren.pack(fill="x", pady=(0, 10))
    
    tk.Label(pnl_der_tren, text="Vagones (Lista ej: 100,100):", bg=cfg.col_Bg).pack(anchor="w")
    entry_vagones = tk.Entry(pnl_der_tren)
    entry_vagones.pack(fill="x", pady=(0, 10))

    # Campo de Solo Lectura (Flujo Acumulado)
    tk.Label(pnl_der_tren, text="Flujo Acumulado (Solo Lectura):", bg=cfg.col_Bg).pack(anchor="w")
    entry_flujo = tk.Entry(pnl_der_tren, bg="#eeeeee")
    entry_flujo.insert(0, "0")
    entry_flujo.config(state="readonly")
    entry_flujo.pack(fill="x", pady=(0, 20))

    # Botones
    tk.Button(pnl_der_tren, text="Crear Tren", bg=cfg.col_Avanzar, font=cfg.font_Boton).pack(fill="x", pady=5)
    tk.Button(pnl_der_tren, text="Eliminar Tren", bg="#ffcccc").pack(fill="x", pady=5)
    tk.Button(pnl_der_tren, text="Guardar Cambios").pack(fill="x", pady=5)


    # =======================================================
    # PESTAÑA 3: RUTAS
    # =======================================================
    
    # --- Panel Izquierdo (Lista) ---
    pnl_izq_ruta = tk.Frame(tab_rutas, bg=cfg.col_Bg, width=200)
    pnl_izq_ruta.pack(side="left", fill="y", padx=5, pady=5)
    
    tk.Label(pnl_izq_ruta, text="Rutas", font=("Arial", 10, "bold"), bg=cfg.col_Bg).pack(anchor="w")
    lista_rutas = tk.Listbox(pnl_izq_ruta, width=25)
    lista_rutas.pack(expand=True, fill="both", pady=5)

    # --- Panel Derecho (Formulario) ---
    pnl_der_ruta = tk.Frame(tab_rutas, bg=cfg.col_Bg)
    pnl_der_ruta.pack(side="right", expand=True, fill="both", padx=10, pady=5)

    # Campos (Basado en models/ruta.py: origen, destino, longitud)
    # Aquí usamos DROPDOWNS para elegir estaciones, no texto libre.
    
    tk.Label(pnl_der_ruta, text="Estación de Origen:", bg=cfg.col_Bg).pack(anchor="w")
    combo_origen = ttk.Combobox(pnl_der_ruta, values=["Est. Central", "Est. Rancagua"], state="readonly")
    combo_origen.pack(fill="x", pady=(0, 10))

    tk.Label(pnl_der_ruta, text="Estación de Destino:", bg=cfg.col_Bg).pack(anchor="w")
    combo_destino = ttk.Combobox(pnl_der_ruta, values=["Est. Central", "Est. Rancagua"], state="readonly")
    combo_destino.pack(fill="x", pady=(0, 10))

    tk.Label(pnl_der_ruta, text="Longitud (kms):", bg=cfg.col_Bg).pack(anchor="w")
    entry_km = tk.Entry(pnl_der_ruta)
    entry_km.pack(fill="x", pady=(0, 20))

    # Botones
    tk.Button(pnl_der_ruta, text="Crear Ruta", bg=cfg.col_Avanzar, font=cfg.font_Boton).pack(fill="x", pady=5)
    tk.Button(pnl_der_ruta, text="Eliminar Ruta", bg="#ffcccc").pack(fill="x", pady=5)
    tk.Button(pnl_der_ruta, text="Guardar Cambios").pack(fill="x", pady=5)