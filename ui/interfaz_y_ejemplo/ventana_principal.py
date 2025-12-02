import tkinter as tk
from config.configuracion import configuracion as cfg
from .ventana_simulador import abrir_simulador
from .ventana_cargadatos import abrir_cargadatos
from logic.estado_simulacion import EstadoSimulacion
from logic.motor_simulacion import MotorSimulacion

def interfaz_principal():

    INICIO = tk.Tk()
    INICIO.title("Entrada")
    INICIO.geometry(cfg.size_Start)

    tk.Label(
        INICIO, text="""Sistema de simulacion de trafico ferroviario""",
        font=cfg.font_Titulo,
        padx=100, pady=40
    ).pack()

    def iniciar_motor_y_ventana():
        estado = EstadoSimulacion()
        estado.gestor_entidades.cargar_datos_iniciales_rf04()
        
        motor = MotorSimulacion(estado.gestor_entidades, estado)
        motor.iniciar_simulacion()
        
        abrir_simulador(INICIO, motor, estado)

    tk.Button(
        INICIO, text="INICIAR SIMULACION",
        width=cfg.size_BotonST,
        height=cfg.size_BotonH,
        foreground=cfg.col_Boton2,
        bg=cfg.col_Boton1,
        font=cfg.font_Boton,
        command=iniciar_motor_y_ventana
    ).pack(pady=5)

    tk.Button(
        INICIO, text="Cargar Simulacion",
        width=cfg.size_BotonST,
        height=cfg.size_BotonH,
        font=cfg.font_Boton,
        command=lambda: abrir_cargadatos(INICIO)
    ).pack(pady=5)

    INICIO.mainloop()