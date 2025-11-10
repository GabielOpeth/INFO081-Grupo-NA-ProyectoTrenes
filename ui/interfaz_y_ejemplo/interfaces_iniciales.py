import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime,time

from config import configuracion as cfg


def interfaz_simulador():
    ventana=tk.Tk()
    ventana.title("Ferrocarriles")
    ventana.geometry(cfg.size_Sim)   
    tk.Label(ventana,text= "Primera prueba",padx=1000,pady=1000)

    ntb_tabulador = ttk.Notebook(ventana)

    tab1 = tk.Frame(ntb_tabulador, bg=cfg.col_Bg, width=cfg.Tab_width, height=cfg.Tab_height)
    tab2 = tk.Frame(ntb_tabulador, bg=cfg.col_Bg, width=cfg.Tab_width, height=cfg.Tab_height)

    ntb_tabulador.add(tab1, text="Simulacion")
    ntb_tabulador.add(tab2, text="Ayuda")
    ntb_tabulador.pack(expand=1, fill="both")
    boton1 = tk.Button(tab1, text=("HORA:",datetime.now()),width=30,height=1, font=cfg.font_Hora)
    boton1.place(x=0,y=0)
    boton2= tk.Button(tab1,text="Avanzar turno",width=35,height=1,font=cfg.font_Avanzar)
    boton2.place(x=0,y=26)

    ventana.mainloop()

def interfaz_cargadatos():
    carga_pantalla=tk.Tk()
    carga_pantalla.title("CARGAR DATOS")
    carga_pantalla.geometry(cfg.size_Load)    
    tk.Label(carga_pantalla, text="Ingresa el nombre del archivo guardado:",
    font=cfg.font_Label).pack(pady=10)
    entrada = tk.Entry(carga_pantalla, font=cfg.font_Label)
    entrada.pack(padx=20, pady=10, fill="x", expand=True)
    carga_pantalla.mainloop()

def interfaz_principal():
    INICIO=tk.Tk()
    INICIO.title("Entrada")
    INICIO.geometry(cfg.size_Start)

    tk.Label(
        INICIO, text="""Sistema de simulacion de trafico ferroviario""",
        font=cfg.font_Titulo, 
        padx=100, pady=40
    ).pack()

    tk.Button(
        INICIO, text="INICIAR SIMULACION",
        width=cfg.size_BotonST,
        height=cfg.size_BotonH,
        foreground=cfg.col_Boton2,
        bg=cfg.col_Boton1,            font=cfg.col_Boton1,
        command=lambda: interfaz_simulador()
    ).pack(pady=5)

    tk.Button(
        INICIO, text="Cargar Simulacion",
        width=cfg.size_BotonST,
        height=cfg.size_BotonH,
        font=cfg.font_Boton,
        command=lambda: interfaz_cargadatos()
    ).pack(pady=5)


    INICIO.mainloop()


#Llamado de ejemplo (eliminado)

