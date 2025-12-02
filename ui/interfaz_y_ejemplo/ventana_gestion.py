import tkinter as tk
from tkinter import ttk, messagebox
from config.configuracion import configuracion as cfg
from models.estacion import GestorEstaciones

gestor_est_local = GestorEstaciones() 

def abrir_gestion_entidades(parentW, tab_inicial=0):

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

    def actualizar_lista_estaciones():
        lista_estaciones.delete(0, tk.END)
        todas = gestor_est_local.obtener_todas()
        for est in todas:
            lista_estaciones.insert(tk.END, f"{est.id} - {est.nombre}")

    def limpiar_campos():
        entry_nombre_est.delete(0, tk.END)
        entry_pob_est.delete(0, tk.END)

    def al_seleccionar_estacion(event):
        seleccion = lista_estaciones.curselection()
        if seleccion:
            texto = lista_estaciones.get(seleccion)
            try:
                id_est = int(texto.split(" - ")[0])
                obj = gestor_est_local.consultar(id_est)
                if obj:
                    limpiar_campos()
                    entry_nombre_est.insert(0, obj.nombre)
                    entry_pob_est.insert(0, str(obj.poblacion))
            except ValueError:
                pass

    def crear_estacion_click():
        nombre = entry_nombre_est.get()
        pob_str = entry_pob_est.get()

        if not nombre or not pob_str:
            messagebox.showwarning("Datos incompletos", "Por favor ingresa nombre y población")
            return
        
        if not pob_str.isdigit():
            messagebox.showerror("Error", "La población debe ser un número")
            return

        vias_default = {'Norte': 'Libre', 'Sur': 'Libre'}
        gestor_est_local.crear(nombre, int(pob_str), vias_default)
        
        actualizar_lista_estaciones()
        limpiar_campos()
        messagebox.showinfo("Éxito", "Estación creada correctamente.")

    def eliminar_estacion_click():
        seleccion = lista_estaciones.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una estación de la lista para eliminar.")
            return
        
        texto = lista_estaciones.get(seleccion)
        try:
            id_est = int(texto.split(" - ")[0])
            
            if messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar la estación {texto}?"):
                exito, msg = gestor_est_local.eliminar(id_est)
                if exito:
                    actualizar_lista_estaciones()
                    limpiar_campos()
                    messagebox.showinfo("Eliminado", msg)
                else:
                    messagebox.showerror("Error", msg)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def guardar_cambios_click():
        seleccion = lista_estaciones.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una estación de la lista para editar.")
            return

        texto = lista_estaciones.get(seleccion)
        try:
            id_est = int(texto.split(" - ")[0])

            nuevo_nombre = entry_nombre_est.get()
            nueva_pob = entry_pob_est.get()

            if not nuevo_nombre or not nueva_pob:
                messagebox.showwarning("Error", "Los campos no pueden estar vacíos")
                return

            exito, msg = gestor_est_local.modificar(id_est, nombre=nuevo_nombre, poblacion=int(nueva_pob))
            
            if exito:
                actualizar_lista_estaciones()
                limpiar_campos()
                messagebox.showinfo("Actualizado", "Cambios guardados correctamente.")
            else:
                messagebox.showerror("Error", msg)
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al guardar: {e}")

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

    btn_vias = tk.Button(pnl_der_est, text="Configurar Vías de Estación", bg="#e1e1e1")
    btn_vias.pack(fill="x", pady=(0, 10))

    tk.Label(pnl_der_est, text="Generador de Demanda (RF05):", bg=cfg.col_Bg).pack(anchor="w")
    combo_demanda = ttk.Combobox(pnl_der_est, values=["Generador Base", "Hora Punta", "Fin de Semana"], state="readonly")
    combo_demanda.current(0)
    combo_demanda.pack(fill="x", pady=(0, 20))

    btn_crear_est = tk.Button(pnl_der_est, 
                              text="Crear Estación", 
                              bg=cfg.col_Avanzar, 
                              font=cfg.font_Boton,
                              command=crear_estacion_click)
    btn_crear_est.pack(fill="x", pady=5)
    
    btn_eliminar_est = tk.Button(pnl_der_est, 
                                 text="Eliminar Estación", 
                                 bg="#ffcccc",
                                 command=eliminar_estacion_click)
    btn_eliminar_est.pack(fill="x", pady=5)

    btn_guardar_est = tk.Button(pnl_der_est, 
                                text="Guardar Cambios",
                                command=guardar_cambios_click)
    btn_guardar_est.pack(fill="x", pady=5)

    actualizar_lista_estaciones()

    pnl_izq_tren = tk.Frame(tab_trenes, bg=cfg.col_Bg, width=200)
    pnl_izq_tren.pack(side="left", fill="y", padx=5, pady=5)
    tk.Label(pnl_izq_tren, text="Trenes", font=("Arial", 10, "bold"), bg=cfg.col_Bg).pack(anchor="w")
    lista_trenes = tk.Listbox(pnl_izq_tren, width=25)
    lista_trenes.pack(expand=True, fill="both", pady=5)

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

    tk.Label(pnl_der_tren, text="Flujo Acumulado (Solo Lectura):", bg=cfg.col_Bg).pack(anchor="w")
    entry_flujo = tk.Entry(pnl_der_tren, bg="#eeeeee")
    entry_flujo.insert(0, "0")
    entry_flujo.config(state="readonly")
    entry_flujo.pack(fill="x", pady=(0, 20))

    tk.Button(pnl_der_tren, text="Crear Tren", bg=cfg.col_Avanzar, font=cfg.font_Boton).pack(fill="x", pady=5)
    tk.Button(pnl_der_tren, text="Eliminar Tren", bg="#ffcccc").pack(fill="x", pady=5)
    tk.Button(pnl_der_tren, text="Guardar Cambios").pack(fill="x", pady=5)

    pnl_izq_ruta = tk.Frame(tab_rutas, bg=cfg.col_Bg, width=200)
    pnl_izq_ruta.pack(side="left", fill="y", padx=5, pady=5)
    tk.Label(pnl_izq_ruta, text="Rutas", font=("Arial", 10, "bold"), bg=cfg.col_Bg).pack(anchor="w")
    lista_rutas = tk.Listbox(pnl_izq_ruta, width=25)
    lista_rutas.pack(expand=True, fill="both", pady=5)

    pnl_der_ruta = tk.Frame(tab_rutas, bg=cfg.col_Bg)
    pnl_der_ruta.pack(side="right", expand=True, fill="both", padx=10, pady=5)

    tk.Label(pnl_der_ruta, text="Estación de Origen:", bg=cfg.col_Bg).pack(anchor="w")
    combo_origen = ttk.Combobox(pnl_der_ruta, values=["Est. Central", "Est. Rancagua"], state="readonly")
    combo_origen.pack(fill="x", pady=(0, 10))

    tk.Label(pnl_der_ruta, text="Estación de Destino:", bg=cfg.col_Bg).pack(anchor="w")
    combo_destino = ttk.Combobox(pnl_der_ruta, values=["Est. Central", "Est. Rancagua"], state="readonly")
    combo_destino.pack(fill="x", pady=(0, 10))

    tk.Label(pnl_der_ruta, text="Longitud (kms):", bg=cfg.col_Bg).pack(anchor="w")
    entry_km = tk.Entry(pnl_der_ruta)
    entry_km.pack(fill="x", pady=(0, 20))

    tk.Button(pnl_der_ruta, text="Crear Ruta", bg=cfg.col_Avanzar, font=cfg.font_Boton).pack(fill="x", pady=5)
    tk.Button(pnl_der_ruta, text="Eliminar Ruta", bg="#ffcccc").pack(fill="x", pady=5)
    tk.Button(pnl_der_ruta, text="Guardar Cambios").pack(fill="x", pady=5)