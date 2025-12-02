import tkinter as tk
from tkinter import ttk, messagebox
from config.configuracion import configuracion as cfg

# Ya no necesitamos crear instancias locales vacías aquí.
# Recibiremos el "cerebro" real como parámetro.

def abrir_gestion_entidades(parentW, gestor_entidades_principal, tab_inicial=0):
    """
    Ahora recibe 'gestor_entidades_principal', que es el objeto que tiene
    los datos reales de la simulación.
    """

    ventana = tk.Toplevel(parentW)
    ventana.title("Gestión de Datos del Sistema")
    ventana.geometry(cfg.size_Gestion)
    ventana.grab_set()

    # --- CONTENEDOR DE PESTAÑAS ---
    notebook = ttk.Notebook(ventana)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    tab_estaciones = tk.Frame(notebook, bg=cfg.col_Bg)
    tab_trenes = tk.Frame(notebook, bg=cfg.col_Bg)
    tab_rutas = tk.Frame(notebook, bg=cfg.col_Bg)

    notebook.add(tab_estaciones, text="Estaciones")
    notebook.add(tab_trenes, text="Trenes")
    notebook.add(tab_rutas, text="Rutas")

    notebook.select(tab_inicial)

    # =======================================================
    # FUNCIONES AUXILIARES (Conectadas al Gestor Real)
    # =======================================================
    def obtener_nombres_estaciones():
        # Usamos gestor_entidades_principal.gestor_estaciones
        return [f"{e.id}-{e.nombre}" for e in gestor_entidades_principal.gestor_estaciones.obtener_todas()]

    def refrescar_combos_rutas():
        lista = obtener_nombres_estaciones()
        try:
            combo_origen['values'] = lista
            combo_destino['values'] = lista
        except (NameError, UnboundLocalError):
            pass 

    # =======================================================
    # LÓGICA: ESTACIONES
    # =======================================================
    
    def actualizar_lista_estaciones():
        lista_estaciones.delete(0, tk.END)
        # CONEXIÓN REAL AQUÍ:
        todas = gestor_entidades_principal.gestor_estaciones.obtener_todas()
        for est in todas:
            lista_estaciones.insert(tk.END, f"{est.id} - {est.nombre}")
        refrescar_combos_rutas()

    def limpiar_campos_est():
        entry_nombre_est.delete(0, tk.END)
        entry_pob_est.delete(0, tk.END)

    def al_seleccionar_estacion(event):
        seleccion = lista_estaciones.curselection()
        if seleccion:
            texto = lista_estaciones.get(seleccion)
            try:
                id_est = int(texto.split(" - ")[0])
                obj = gestor_entidades_principal.gestor_estaciones.consultar(id_est)
                if obj:
                    limpiar_campos_est()
                    entry_nombre_est.insert(0, obj.nombre)
                    entry_pob_est.insert(0, str(obj.poblacion))
            except ValueError: pass

    def crear_estacion_click():
        nombre = entry_nombre_est.get()
        pob = entry_pob_est.get()
        if not nombre or not pob.isdigit():
            messagebox.showwarning("Error", "Datos inválidos en Estación")
            return
        
        # Guardamos en el gestor principal
        gestor_entidades_principal.gestor_estaciones.crear(nombre, int(pob), {'Norte': 'Libre', 'Sur': 'Libre'})
        
        actualizar_lista_estaciones()
        limpiar_campos_est()
        messagebox.showinfo("Éxito", "Estación creada y guardada en memoria.")

    def eliminar_estacion_click():
        sel = lista_estaciones.curselection()
        if not sel: return
        id_est = int(lista_estaciones.get(sel).split(" - ")[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar estación?"):
            gestor_entidades_principal.gestor_estaciones.eliminar(id_est)
            actualizar_lista_estaciones()
            limpiar_campos_est()

    def guardar_estacion_click():
        sel = lista_estaciones.curselection()
        if not sel: return
        id_est = int(lista_estaciones.get(sel).split(" - ")[0])
        nombre = entry_nombre_est.get()
        pob = entry_pob_est.get()
        
        if nombre and pob.isdigit():
            gestor_entidades_principal.gestor_estaciones.modificar(id_est, nombre=nombre, poblacion=int(pob))
            actualizar_lista_estaciones()
            limpiar_campos_est()
            messagebox.showinfo("Éxito", "Cambios guardados")

    # =======================================================
    # LÓGICA: TRENES
    # =======================================================

    def actualizar_lista_trenes():
        lista_trenes.delete(0, tk.END)
        for tren in gestor_entidades_principal.gestor_trenes.obtener_todos():
            lista_trenes.insert(tk.END, f"{tren.id} - {tren.nombre}")

    def limpiar_campos_tren():
        entry_nom_tren.delete(0, tk.END)
        entry_vel_tren.delete(0, tk.END)
        entry_vagones.delete(0, tk.END)

    def al_seleccionar_tren(event):
        sel = lista_trenes.curselection()
        if sel:
            texto = lista_trenes.get(sel)
            try:
                id_tren = int(texto.split(" - ")[0])
                obj = gestor_entidades_principal.gestor_trenes.consultar(id_tren)
                if obj:
                    limpiar_campos_tren()
                    entry_nom_tren.insert(0, obj.nombre)
                    entry_vel_tren.insert(0, str(obj.velocidad))
                    vagones_str = ",".join(map(str, obj.vagones)) if isinstance(obj.vagones, list) else str(obj.vagones)
                    entry_vagones.insert(0, vagones_str)
            except ValueError: pass

    def parsear_vagones(texto):
        try:
            return [int(x.strip()) for x in texto.split(',')]
        except:
            return None

    def crear_tren_click():
        nombre = entry_nom_tren.get()
        vel = entry_vel_tren.get()
        vagones_lista = parsear_vagones(entry_vagones.get())

        if not nombre or not vel.isdigit() or not vagones_lista:
            messagebox.showwarning("Error", "Datos inválidos (Vagones ej: 100,100)")
            return

        gestor_entidades_principal.gestor_trenes.crear(int(vel), nombre, vagones_lista)
        actualizar_lista_trenes()
        limpiar_campos_tren()
        messagebox.showinfo("Éxito", "Tren creado")

    def eliminar_tren_click():
        sel = lista_trenes.curselection()
        if not sel: return
        id_tren = int(lista_trenes.get(sel).split(" - ")[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar tren?"):
            gestor_entidades_principal.gestor_trenes.eliminar(id_tren)
            actualizar_lista_trenes()
            limpiar_campos_tren()

    def guardar_tren_click():
        sel = lista_trenes.curselection()
        if not sel: return
        id_tren = int(lista_trenes.get(sel).split(" - ")[0])
        nombre = entry_nom_tren.get()
        vel = entry_vel_tren.get()
        vagones_lista = parsear_vagones(entry_vagones.get())

        if nombre and vel.isdigit() and vagones_lista:
            gestor_entidades_principal.gestor_trenes.modificar(id_tren, nombre=nombre, velocidad=int(vel), vagones=vagones_lista)
            actualizar_lista_trenes()
            limpiar_campos_tren()
            messagebox.showinfo("Éxito", "Tren actualizado")

    # =======================================================
    # LÓGICA: RUTAS
    # =======================================================

    def actualizar_lista_rutas():
        lista_rutas.delete(0, tk.END)
        for ruta in gestor_entidades_principal.gestor_rutas.obtener_todas():
            origen_nm = ruta.origen.nombre if hasattr(ruta.origen, 'nombre') else str(ruta.origen)
            destino_nm = ruta.destino.nombre if hasattr(ruta.destino, 'nombre') else str(ruta.destino)
            lista_rutas.insert(tk.END, f"{ruta.id} - {origen_nm} -> {destino_nm}")

    def limpiar_campos_ruta():
        combo_origen.set('')
        combo_destino.set('')
        entry_km.delete(0, tk.END)

    def al_seleccionar_ruta(event):
        sel = lista_rutas.curselection()
        if sel:
            texto = lista_rutas.get(sel)
            try:
                id_ruta = int(texto.split(" - ")[0])
                obj = gestor_entidades_principal.gestor_rutas.consultar(id_ruta)
                if obj:
                    limpiar_campos_ruta()
                    if hasattr(obj.origen, 'id'):
                        combo_origen.set(f"{obj.origen.id}-{obj.origen.nombre}")
                    if hasattr(obj.destino, 'id'):
                        combo_destino.set(f"{obj.destino.id}-{obj.destino.nombre}")
                    entry_km.insert(0, str(obj.longitud_km))
            except ValueError: pass

    def obtener_estacion_desde_combo(texto_combo):
        if not texto_combo: return None
        try:
            id_est = int(texto_combo.split('-')[0])
            return gestor_entidades_principal.gestor_estaciones.consultar(id_est)
        except: return None

    def crear_ruta_click():
        txt_origen = combo_origen.get()
        txt_destino = combo_destino.get()
        kms = entry_km.get()

        obj_origen = obtener_estacion_desde_combo(txt_origen)
        obj_destino = obtener_estacion_desde_combo(txt_destino)

        if not obj_origen or not obj_destino or not kms.isdigit():
            messagebox.showwarning("Error", "Selecciona origen/destino válidos y kms numéricos")
            return
        
        if obj_origen.id == obj_destino.id:
            messagebox.showwarning("Lógica", "El origen y destino no pueden ser iguales")
            return

        gestor_entidades_principal.gestor_rutas.crear(obj_origen, obj_destino, int(kms))
        actualizar_lista_rutas()
        limpiar_campos_ruta()
        messagebox.showinfo("Éxito", "Ruta creada")

    def eliminar_ruta_click():
        sel = lista_rutas.curselection()
        if not sel: return
        id_ruta = int(lista_rutas.get(sel).split(" - ")[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar ruta?"):
            gestor_entidades_principal.gestor_rutas.eliminar(id_ruta)
            actualizar_lista_rutas()
            limpiar_campos_ruta()

    def guardar_ruta_click():
        sel = lista_rutas.curselection()
        if not sel: return
        id_ruta = int(lista_rutas.get(sel).split(" - ")[0])
        kms = entry_km.get()
        
        if kms.isdigit():
            gestor_entidades_principal.gestor_rutas.modificar(id_ruta, longitud_km=int(kms))
            actualizar_lista_rutas()
            limpiar_campos_ruta()
            messagebox.showinfo("Éxito", "Kms actualizados")


    # =======================================================
    # DISEÑO PESTAÑA 1: ESTACIONES
    # =======================================================
    pnl_izq_est = tk.Frame(tab_estaciones, bg=cfg.col_Bg, width=200)
    pnl_izq_est.pack(side="left", fill="y", padx=5, pady=5)
    tk.Label(pnl_izq_est, text="Estaciones", font=("Arial", 10, "bold"), bg=cfg.col_Bg).pack(anchor="w")
    lista_estaciones = tk.Listbox(pnl_izq_est, width=25)
    lista_estaciones.pack(expand=True, fill="both", pady=5)
    lista_estaciones.bind('<<ListboxSelect>>', al_seleccionar_estacion)
    
    pnl_der_est = tk.Frame(tab_estaciones, bg=cfg.col_Bg)
    pnl_der_est.pack(side="right", expand=True, fill="both", padx=10, pady=5)

    tk.Label(pnl_der_est, text="Nombre:", bg=cfg.col_Bg).pack(anchor="w")
    entry_nombre_est = tk.Entry(pnl_der_est)
    entry_nombre_est.pack(fill="x", pady=(0, 10))

    tk.Label(pnl_der_est, text="Población:", bg=cfg.col_Bg).pack(anchor="w")
    entry_pob_est = tk.Entry(pnl_der_est)
    entry_pob_est.pack(fill="x", pady=(0, 10))

    tk.Button(pnl_der_est, text="Configurar Vías", bg="#e1e1e1").pack(fill="x", pady=(0, 10))
    
    tk.Label(pnl_der_est, text="Generador de Demanda:", bg=cfg.col_Bg).pack(anchor="w")
    ttk.Combobox(pnl_der_est, values=["Base"], state="readonly").pack(fill="x", pady=(0, 20))

    tk.Button(pnl_der_est, text="Crear Estación", bg=cfg.col_Avanzar, font=cfg.font_Boton, command=crear_estacion_click).pack(fill="x", pady=5)
    tk.Button(pnl_der_est, text="Eliminar Estación", bg="#ffcccc", command=eliminar_estacion_click).pack(fill="x", pady=5)
    tk.Button(pnl_der_est, text="Guardar Cambios", command=guardar_estacion_click).pack(fill="x", pady=5)

    actualizar_lista_estaciones()

    # =======================================================
    # DISEÑO PESTAÑA 2: TRENES
    # =======================================================
    pnl_izq_tren = tk.Frame(tab_trenes, bg=cfg.col_Bg, width=200)
    pnl_izq_tren.pack(side="left", fill="y", padx=5, pady=5)
    
    tk.Label(pnl_izq_tren, text="Trenes", font=("Arial", 10, "bold"), bg=cfg.col_Bg).pack(anchor="w")
    lista_trenes = tk.Listbox(pnl_izq_tren, width=25)
    lista_trenes.pack(expand=True, fill="both", pady=5)
    lista_trenes.bind('<<ListboxSelect>>', al_seleccionar_tren)

    pnl_der_tren = tk.Frame(tab_trenes, bg=cfg.col_Bg)
    pnl_der_tren.pack(side="right", expand=True, fill="both", padx=10, pady=5)

    tk.Label(pnl_der_tren, text="Nombre del Tren:", bg=cfg.col_Bg).pack(anchor="w")
    entry_nom_tren = tk.Entry(pnl_der_tren)
    entry_nom_tren.pack(fill="x", pady=(0, 10))

    tk.Label(pnl_der_tren, text="Velocidad (km/h):", bg=cfg.col_Bg).pack(anchor="w")
    entry_vel_tren = tk.Entry(pnl_der_tren)
    entry_vel_tren.pack(fill="x", pady=(0, 10))
    
    tk.Label(pnl_der_tren, text="Vagones (Lista ej: 100,100):", bg=cfg.col_Bg).pack(anchor="w")
    entry_vagones = tk.Entry(pnl_der_tren)
    entry_vagones.pack(fill="x", pady=(0, 10))

    tk.Label(pnl_der_tren, text="Flujo Acumulado (Lectura):", bg=cfg.col_Bg).pack(anchor="w")
    entry_flujo = tk.Entry(pnl_der_tren, bg="#eeeeee")
    entry_flujo.insert(0, "0")
    entry_flujo.config(state="readonly")
    entry_flujo.pack(fill="x", pady=(0, 20))

    tk.Button(pnl_der_tren, text="Crear Tren", bg=cfg.col_Avanzar, font=cfg.font_Boton, command=crear_tren_click).pack(fill="x", pady=5)
    tk.Button(pnl_der_tren, text="Eliminar Tren", bg="#ffcccc", command=eliminar_tren_click).pack(fill="x", pady=5)
    tk.Button(pnl_der_tren, text="Guardar Cambios", command=guardar_tren_click).pack(fill="x", pady=5)

    actualizar_lista_trenes()

    # =======================================================
    # DISEÑO PESTAÑA 3: RUTAS
    # =======================================================
    pnl_izq_ruta = tk.Frame(tab_rutas, bg=cfg.col_Bg, width=200)
    pnl_izq_ruta.pack(side="left", fill="y", padx=5, pady=5)
    tk.Label(pnl_izq_ruta, text="Rutas", font=("Arial", 10, "bold"), bg=cfg.col_Bg).pack(anchor="w")
    lista_rutas = tk.Listbox(pnl_izq_ruta, width=25)
    lista_rutas.pack(expand=True, fill="both", pady=5)
    lista_rutas.bind('<<ListboxSelect>>', al_seleccionar_ruta)

    pnl_der_ruta = tk.Frame(tab_rutas, bg=cfg.col_Bg)
    pnl_der_ruta.pack(side="right", expand=True, fill="both", padx=10, pady=5)

    tk.Label(pnl_der_ruta, text="Estación de Origen:", bg=cfg.col_Bg).pack(anchor="w")
    combo_origen = ttk.Combobox(pnl_der_ruta, state="readonly")
    combo_origen.pack(fill="x", pady=(0, 10))

    tk.Label(pnl_der_ruta, text="Estación de Destino:", bg=cfg.col_Bg).pack(anchor="w")
    combo_destino = ttk.Combobox(pnl_der_ruta, state="readonly")
    combo_destino.pack(fill="x", pady=(0, 10))

    tk.Label(pnl_der_ruta, text="Longitud (kms):", bg=cfg.col_Bg).pack(anchor="w")
    entry_km = tk.Entry(pnl_der_ruta)
    entry_km.pack(fill="x", pady=(0, 20))

    tk.Button(pnl_der_ruta, text="Crear Ruta", bg=cfg.col_Avanzar, font=cfg.font_Boton, command=crear_ruta_click).pack(fill="x", pady=5)
    tk.Button(pnl_der_ruta, text="Eliminar Ruta", bg="#ffcccc", command=eliminar_ruta_click).pack(fill="x", pady=5)
    tk.Button(pnl_der_ruta, text="Guardar Cambios (Solo Kms)", command=guardar_ruta_click).pack(fill="x", pady=5)

    actualizar_lista_rutas()
    refrescar_combos_rutas()