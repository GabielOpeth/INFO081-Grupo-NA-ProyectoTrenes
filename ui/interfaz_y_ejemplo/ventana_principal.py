import tkinter as tk
from config import configuracion as cfg
from .ventana_simulador import abrir_simulador
from .ventana_cargadatos import abrir_cargadatos

def interfaz_principal():

    #ventana de aplicación
    
    INICIO = tk.Tk()
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
        bg=cfg.col_Boton1,
        

        font=cfg.font_Boton,
        command=lambda: abrir_simulador(INICIO) 
    ).pack(pady=5)

    tk.Button(
        INICIO, text="Cargar Simulacion",
        width=cfg.size_BotonST,
        height=cfg.size_BotonH,
        font=cfg.font_Boton,
        command=lambda: abrir_cargadatos(INICIO)
    ).pack(pady=5)

    # dev note: solo se usa mainloop() en la ventana raiz
    INICIO.mainloop()