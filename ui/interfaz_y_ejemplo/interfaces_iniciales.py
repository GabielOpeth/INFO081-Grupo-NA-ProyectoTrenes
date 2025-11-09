import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime,time


def interfaz_simulador():
    ventana=tk.Tk()
    ventana.title("Ferrocarriles")
    tk.Label(ventana,text= "Primera prueba",padx=1000,pady=1000)

    ntb_tabulador = ttk.Notebook(ventana)
    tab1 = tk.Frame(ntb_tabulador, bg="White", width=1000, height=1000)
    tab2 = tk.Frame(ntb_tabulador, bg="White", width=1000, height=1000)
    ntb_tabulador.add(tab1, text="Simulacion")
    ntb_tabulador.add(tab2, text="Ayuda")
    ntb_tabulador.pack(expand=1, fill="y")
    boton1 = tk.Button(tab1, text=("HORA:",datetime.now()),width=30,height=1, font=("Arial", 10))
    boton1.place(x=0,y=0)
    boton2= tk.Button(tab1,text="Avanzar turno",width=35,height=1,font=("arial",8))
    boton2.place(x=0,y=26)

    ventana.mainloop()

def interfaz_cargadatos():
    carga_pantalla=tk.Tk()
    carga_pantalla.title("CARGAR DATOS")
    tk.Label(carga_pantalla, text="Ingresa el nombre del archivo guardado:",
              font=("Arial", 12)).pack(pady=10)
    entrada = tk.Entry(carga_pantalla, font=("Arial", 12))
    entrada.pack(padx=20, pady=10)
    carga_pantalla.mainloop()

def interfaz_principal():
    INICIO=tk.Tk()
    INICIO.title("Entrada")
    tk.Label(INICIO, text="""Sistema de """
                """simulacion de trafico """
                        """ferroviario""",font=("arial",20),padx=100,pady=100).pack()
    tk.Button(
        INICIO, text="INICIAR SIMULACION",width=50,height=1,foreground="Black", bg="#7fffd4",command=lambda: interfaz_simulador()
    ).pack()

    tk.Button(
        INICIO, text="Cargar Simulacion",width=50,height=1, command=lambda: interfaz_cargadatos()
    ).pack()

    INICIO.mainloop()
#Llamado de ejemplo
interfaz_principal()
