import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime, time
from config import configuracion as cfg

def abrir_simulador (ventana_main):

    #dev msg: usamos Toplevel
    ventana = tk.Toplevel(ventana_main)
    ventana.title("Ferrocarriles")
    ventana.geometry(cfg.size_Sim)
    
    #freeze
    ventana.grab_set() 

    #dev msg: codigo original
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