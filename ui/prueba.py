import tkinter as tk

def interfaz():
    ventana=tk.Tk()
    ventana.title("Ferrocarriles")
    tk.Label(ventana,text= "Primera prueba",padx=1000,pady=1000).pack()
    

def primeraventana():
    INICIO=tk.Tk()
    INICIO.title("Entrada")
    tk.Label(INICIO, text="""Sistema de """
                """simulacion de trafico """
                        """ferroviario""",padx=100,pady=100).pack()
    tk.Button(
        INICIO, text="INICIAR SIMULACION",foreground="Black", bg="#7fffd4",	 command=lambda: interfaz()
    ).pack()

    tk.Button(
        INICIO, text="Cargar Simulacion", command=lambda: interfaz()
    ).pack()

    INICIO.mainloop()

if __name__=="__primeraventana__":
    primeraventana()