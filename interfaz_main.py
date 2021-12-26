import tkinter
from tkinter import *
from typing import NewType
import inicializa as ini
import main as main
import interfaz_clientes as iClientes
import pyodbc


raiz = Tk()

raiz.title("Practica 3 - DDSI")
 


conn = main.conectaBase()

###################################################################################################################################


###################################################################################################################################
miFrame = Frame()
miFrame.pack(expand = "True", fill = "both")
miFrame.config(width = "1080", height = "720", bd = "10", relief = "sunken")

etiquetaInformacion = Label(miFrame, 
font = ("Time News Roman", 10), text = "Bienvenido al centro deportivo Epicardo, por favor, eliga una de las siguientes opciones:")
etiquetaInformacion.place(x = 300, y = 0)

botonInicializar = Button(miFrame, text = "1. Inicializar BBDD", width = "30", 
cursor = "pirate", font = ("Time News Roman", 10), command= lambda: ini.main(conn)).place(x = 450, y = 50)

botonClientes = Button(miFrame, text = "2. Gestión de clientes", width = "30", 
cursor = "pirate", font = ("Time News Roman", 10), command = iClientes.ventanaGestionClientes).place(x = 450, y = 150)

botonEntrenadores = Button(miFrame, text = "3. Gestión de entrenadores", width = "30", 
cursor = "pirate", font = ("Time News Roman", 10)).place(x = 450, y = 250)

botonClases = Button(miFrame, text = "4. Gestión de clases", width = "30", 
cursor = "pirate", font = ("Time News Roman", 10)).place(x = 450, y = 350)

botonInstalaciones = Button(miFrame, text = "5. Gestión de instalaciones", width = "30", 
cursor = "pirate", font = ("Time News Roman", 10)).place(x = 450, y = 450)

botonSalir = Button(miFrame, text = "6. Salir", width = "30", 
cursor = "pirate", font = ("Time News Roman", 10), command = raiz.destroy).place(x = 450, y = 550)

raiz.mainloop()