import tkinter as tk
from config import configuracion as cfg
from tkinter import messagebox
from logic.sistema_guardado_old import SistemaDeGuardado

def abrir_cargadatos(ventana_main):

    # dev msg: cambiamos por Toplevel
    carga_pantalla = tk.Toplevel(ventana_main)
    carga_pantalla.title("CARGAR DATOS")
    carga_pantalla.geometry(cfg.size_Load)
    
    # freeze
    carga_pantalla.grab_set()

    # dev msg: codigo original
    tk.Label(carga_pantalla, text="Ingresa el nombre del archivo guardado:",
             font=cfg.font_Label).pack(pady=10)
             
    entrada = tk.Entry(carga_pantalla, font=cfg.font_Label)
    entrada.pack(padx=20, pady=10, fill="x", expand=True)