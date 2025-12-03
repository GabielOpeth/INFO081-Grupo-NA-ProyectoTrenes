import tkinter as tk
from tkinter import ttk, messagebox
from config.configuracion import configuracion as cfg

# No necesitamos instancias locales aquí, usaremos la principal

def abrir_gestion_entidades(parentW, gestor_entidades_principal, tab_inicial=0):
    """
    Recibe 'gestor_entidades_principal' para editar los datos REALES.
    """

    ventana = tk.Toplevel(parentW)
    ventana.title("Gestión de Datos del Sistema")
    ventana.geometry(cfg.size_Gestion)
    ventana.grab_set()

    notebook = ttk.Notebook(ventana)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    tab_estaciones = tk.Frame(notebook, bg=cfg.col_Bg)
    tab_trenes = tk.Frame(notebook, bg=cfg.col_Bg)
    tab_rutas = tk.Frame(notebook, bg=cfg.col_Bg)

    notebook.add(tab_estaciones, text="Estaciones")
    notebook.add(tab_trenes, text="Trenes")
    notebook.add(tab_rutas, text="Rutas")

    notebook.select(tab_inicial)

    # --- FUNCIONES AUXILIARES ---
    def obtener_nombres_estaciones():
        return [f"{e.id}-{e.nombre}" for e in gestor_entidades_principal.gestor_estaciones.obtener_todas()]

    def refrescar_combos_rutas():
        lista = obtener_nombres_estaciones()
        try:
            combo_origen['values'] = lista
            combo_destino['values'] = lista
        except: pass

    # ==========================================
    # PESTAÑA ESTACIONES
    # ==========================================
    def actualizar_lista_estaciones():
        lista_estaciones.delete(0, tk.END)
        # USAMOS EL GESTOR PRINCIPAL
        for est in gestor_entidades_principal.gestor_estaciones.obtener_todas():
            lista_estaciones.insert(tk.END, f"{est.id} - {est.nombre}")
        refrescar_combos_rutas()

    def limpiar_campos_est():
        entry_nombre_est.delete(0, tk.END)
        entry_pob_est.delete(0, tk.END)

    def al_seleccionar_estacion(event):
        sel = lista_estaciones.curselection()
        if sel:
            texto = lista_estaciones.get(sel)
            try:
                id_est = int(texto.split(" - ")[0])
                obj = gestor_entidades_principal.gestor_estaciones.consultar(id_est)
                if obj:
                    limpiar_campos_est()
                    entry_nombre_est.insert(0, obj.nombre)
                    entry_pob_est.insert(0, str(obj.poblacion))
            except: pass

    def crear_estacion_click():
        if not entry_nombre_est.get() or not entry_pob_est.get().isdigit():
            messagebox.showwarning("Error", "Datos inválidos")
            return
        
        gestor_entidades_principal.gestor_estaciones.crear(
            entry_nombre_est.get(), 
            int(entry_pob_est.get()), 
            {'Norte': 'Libre'}
        )
        actualizar_lista_estaciones()
        limpiar_campos_est()
        messagebox.showinfo("Éxito", "Estación creada")

    def eliminar_estacion_click():
        sel = lista_estaciones.curselection()
        if not sel: return
        id_est = int(lista_estaciones.get(sel).split(" - ")[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar?"):
            gestor_entidades_principal.gestor_estaciones.eliminar(id_est)
            actualizar_lista_estaciones()
            limpiar_campos_est()

    def guardar_estacion_click():
        sel = lista_estaciones.curselection()
        if not sel: return
        id_est = int(lista_estaciones.get(sel).split(" - ")[0])
        if entry_pob_est.get().isdigit():
            gestor_entidades_principal.gestor_estaciones.modificar(
                id_est, 
                nombre=entry_nombre_est.get(), 
                poblacion=int(entry_pob_est.get())
            )
            actualizar_lista_estaciones()
            limpiar_campos_est()
            messagebox.showinfo("Éxito", "Cambios guardados")

    # Layout Estaciones
    pnl_izq_est = tk.Frame(tab_estaciones, bg=cfg.col_Bg, width=200)
    pnl_izq_est.pack(side="left", fill="y", padx=5, pady=5)
    tk.Label(pnl_izq_est, text="Estaciones", font=cfg.font_Boton, bg=cfg.col_Bg).pack(anchor="w")
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

    tk.Button(pnl_der_est, text="Crear Estación", bg=cfg.col_Avanzar, command=crear_estacion_click).pack(fill="x", pady=5)
    tk.Button(pnl_der_est, text="Eliminar Estación", bg="#ffcccc", command=eliminar_estacion_click).pack(fill="x", pady=5)
    tk.Button(pnl_der_est, text="Guardar Cambios", command=guardar_estacion_click).pack(fill="x", pady=5)

    actualizar_lista_estaciones()

    # ==========================================
    # PESTAÑA TRENES
    # ==========================================
    def actualizar_lista_trenes():
        lista_trenes.delete(0, tk.END)
        for t in gestor_entidades_principal.gestor_trenes.obtener_todos():
            lista_trenes.insert(tk.END, f"{t.id} - {t.nombre}")

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
                    vag = ",".join(map(str, obj.vagones)) if isinstance(obj.vagones, list) else str(obj.vagones)
                    entry_vagones.insert(0, vag)
            except: pass

    def crear_tren_click():
        nom = entry_nom_tren.get()
        vel = entry_vel_tren.get()
        vag = entry_vagones.get()
        try:
            vag_lista = [int(x) for x in vag.split(',')]
            if nom and vel.isdigit():
                gestor_entidades_principal.gestor_trenes.crear(int(vel), nom, vag_lista)
                actualizar_lista_trenes()
                limpiar_campos_tren()
                messagebox.showinfo("Éxito", "Tren creado")
        except: messagebox.showerror("Error", "Formato de vagones incorrecto (ej: 100,100)")

    def eliminar_tren_click():
        sel = lista_trenes.curselection()
        if sel:
            id_t = int(lista_trenes.get(sel).split(" - ")[0])
            if messagebox.askyesno("Confirmar", "¿Eliminar?"):
                gestor_entidades_principal.gestor_trenes.eliminar(id_t)
                actualizar_lista_trenes()
                limpiar_campos_tren()

    def guardar_tren_click():
        sel = lista_trenes.curselection()
        if sel:
            id_t = int(lista_trenes.get(sel).split(" - ")[0])
            try:
                vag_lista = [int(x) for x in entry_vagones.get().split(',')]
                gestor_entidades_principal.gestor_trenes.modificar(
                    id_t, 
                    nombre=entry_nom_tren.get(),
                    velocidad=int(entry_vel_tren.get()),
                    vagones=vag_lista
                )
                actualizar_lista_trenes()
                limpiar_campos_tren()
                messagebox.showinfo("Éxito", "Actualizado")
            except: pass

    # Organizador Trenes
    pnl_izq_tren = tk.Frame(tab_trenes, bg=cfg.col_Bg, width=200)
    pnl_izq_tren.pack(side="left", fill="y", padx=5, pady=5)
    tk.Label(pnl_izq_tren, text="Trenes", font=cfg.font_Boton, bg=cfg.col_Bg).pack(anchor="w")
    lista_trenes = tk.Listbox(pnl_izq_tren, width=25)
    lista_trenes.pack(expand=True, fill="both", pady=5)
    lista_trenes.bind('<<ListboxSelect>>', al_seleccionar_tren)

    pnl_der_tren = tk.Frame(tab_trenes, bg=cfg.col_Bg)
    pnl_der_tren.pack(side="right", expand=True, fill="both", padx=10, pady=5)
    
    tk.Label(pnl_der_tren, text="Nombre:", bg=cfg.col_Bg).pack(anchor="w")
    entry_nom_tren = tk.Entry(pnl_der_tren)
    entry_nom_tren.pack(fill="x")
    tk.Label(pnl_der_tren, text="Velocidad:", bg=cfg.col_Bg).pack(anchor="w")
    entry_vel_tren = tk.Entry(pnl_der_tren)
    entry_vel_tren.pack(fill="x")
    tk.Label(pnl_der_tren, text="Vagones (100,100):", bg=cfg.col_Bg).pack(anchor="w")
    entry_vagones = tk.Entry(pnl_der_tren)
    entry_vagones.pack(fill="x", pady=(0,10))

    tk.Button(pnl_der_tren, text="Crear Tren", bg=cfg.col_Avanzar, command=crear_tren_click).pack(fill="x", pady=5)
    tk.Button(pnl_der_tren, text="Eliminar Tren", bg="#ffcccc", command=eliminar_tren_click).pack(fill="x", pady=5)
    tk.Button(pnl_der_tren, text="Guardar Cambios", command=guardar_tren_click).pack(fill="x", pady=5)

    actualizar_lista_trenes()

    # ==========================================
    # PESTAÑA RUTAS
    # ==========================================
    def actualizar_lista_rutas():
        lista_rutas.delete(0, tk.END)
        for r in gestor_entidades_principal.gestor_rutas.obtener_todas():
            o = r.origen.nombre if hasattr(r.origen, 'nombre') else "?"
            d = r.destino.nombre if hasattr(r.destino, 'nombre') else "?"
            lista_rutas.insert(tk.END, f"{r.id} - {o} -> {d}")

    def limpiar_campos_ruta():
        combo_origen.set('')
        combo_destino.set('')
        entry_km.delete(0, tk.END)

    def al_seleccionar_ruta(event):
        sel = lista_rutas.curselection()
        if sel:
            texto = lista_rutas.get(sel)
            try:
                id_r = int(texto.split(" - ")[0])
                obj = gestor_entidades_principal.gestor_rutas.consultar(id_r)
                if obj:
                    limpiar_campos_ruta()
                    if hasattr(obj.origen, 'nombre'): combo_origen.set(f"{obj.origen.id}-{obj.origen.nombre}")
                    if hasattr(obj.destino, 'nombre'): combo_destino.set(f"{obj.destino.id}-{obj.destino.nombre}")
                    entry_km.insert(0, str(obj.longitud_km))
            except: pass

    def crear_ruta_click():
        try:
            id_o = int(combo_origen.get().split('-')[0])
            id_d = int(combo_destino.get().split('-')[0])
            kms = int(entry_km.get())
            
            obj_o = gestor_entidades_principal.gestor_estaciones.consultar(id_o)
            obj_d = gestor_entidades_principal.gestor_estaciones.consultar(id_d)
            
            if obj_o and obj_d:
                gestor_entidades_principal.gestor_rutas.crear(obj_o, obj_d, kms)
                actualizar_lista_rutas()
                limpiar_campos_ruta()
                messagebox.showinfo("Éxito", "Ruta creada")
        except: messagebox.showerror("Error", "Selecciona origen/destino válidos")

    def eliminar_ruta_click():
        sel = lista_rutas.curselection()
        if sel:
            id_r = int(lista_rutas.get(sel).split(" - ")[0])
            if messagebox.askyesno("Confirmar", "¿Eliminar?"):
                gestor_entidades_principal.gestor_rutas.eliminar(id_r)
                actualizar_lista_rutas()
                limpiar_campos_ruta()

    def guardar_ruta_click():
        sel = lista_rutas.curselection()
        if sel:
            id_r = int(lista_rutas.get(sel).split(" - ")[0])
            if entry_km.get().isdigit():
                gestor_entidades_principal.gestor_rutas.modificar(id_r, longitud_km=int(entry_km.get()))
                actualizar_lista_rutas()
                limpiar_campos_ruta()
                messagebox.showinfo("Éxito", "Kms actualizados")

    # Organizador Rutas
    pnl_izq_ruta = tk.Frame(tab_rutas, bg=cfg.col_Bg, width=200)
    pnl_izq_ruta.pack(side="left", fill="y", padx=5, pady=5)
    tk.Label(pnl_izq_ruta, text="Rutas", font=cfg.font_Boton, bg=cfg.col_Bg).pack(anchor="w")
    lista_rutas = tk.Listbox(pnl_izq_ruta, width=25)
    lista_rutas.pack(expand=True, fill="both", pady=5)
    lista_rutas.bind('<<ListboxSelect>>', al_seleccionar_ruta)

    pnl_der_ruta = tk.Frame(tab_rutas, bg=cfg.col_Bg)
    pnl_der_ruta.pack(side="right", expand=True, fill="both", padx=10, pady=5)
    
    tk.Label(pnl_der_ruta, text="Origen:", bg=cfg.col_Bg).pack(anchor="w")
    combo_origen = ttk.Combobox(pnl_der_ruta, state="readonly")
    combo_origen.pack(fill="x")
    tk.Label(pnl_der_ruta, text="Destino:", bg=cfg.col_Bg).pack(anchor="w")
    combo_destino = ttk.Combobox(pnl_der_ruta, state="readonly")
    combo_destino.pack(fill="x")
    tk.Label(pnl_der_ruta, text="Kms:", bg=cfg.col_Bg).pack(anchor="w")
    entry_km = tk.Entry(pnl_der_ruta)
    entry_km.pack(fill="x", pady=(0,10))

    tk.Button(pnl_der_ruta, text="Crear Ruta", bg=cfg.col_Avanzar, command=crear_ruta_click).pack(fill="x", pady=5)
    tk.Button(pnl_der_ruta, text="Eliminar Ruta", bg="#ffcccc", command=eliminar_ruta_click).pack(fill="x", pady=5)
    tk.Button(pnl_der_ruta, text="Guardar Cambios (Solo Kms)", command=guardar_ruta_click).pack(fill="x", pady=5)

    actualizar_lista_rutas()
    refrescar_combos_rutas()