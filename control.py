
import tkinter as tk

# Ventana principal
ventana = tk.Tk()
ventana.title("Control del Robot Agrícola")
ventana.geometry("400x350")
ventana.resizable(False, False)

# Estado del sistema
sistema_activo = False

def encender_sistema():
    global sistema_activo
    sistema_activo = True
    estado.config(text="SISTEMA ACTIVO", fg="green")
    boton_on.config(state="disabled")
    boton_off.config(state="normal")

def apagar_sistema():
    global sistema_activo
    sistema_activo = False
    estado.config(text="SISTEMA APAGADO", fg="red")
    boton_on.config(state="normal")
    boton_off.config(state="disabled")

# Título
titulo = tk.Label(
    ventana,
    text="ROBOT AGRÍCOLA",
    font=("Arial", 18, "bold")
)
titulo.pack(pady=20)

# Estado
estado = tk.Label(
    ventana,
    text="SISTEMA APAGADO",
    fg="red",
    font=("Arial", 14, "bold")
)
estado.pack(pady=15)

# Botón ON
boton_on = tk.Button(
    ventana,
    text="ENCENDER SISTEMA",
    bg="green",
    fg="white",
    font=("Arial", 12),
    width=22,
    command=encender_sistema
)
boton_on.pack(pady=8)

# Botón OFF
boton_off = tk.Button(
    ventana,
    text="APAGAR SISTEMA",
    bg="red",
    fg="white",
    font=("Arial", 12),
    width=22,
    state="disabled",
    command=apagar_sistema
)
boton_off.pack(pady=8)

ventana.mainloop()
