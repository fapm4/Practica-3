import tkinter
from tkinter import *
from typing import NewType
import inicializa as ini
import subsistema_clientes as clientes
import pyodbc


raiz = Tk()

raiz.title("Practica 3 - DDSI")
#raiz.geometry("1080x720")

def conectaBase():
    try:
        conn = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0.ugr.es;Service Name=practbd.oracle0.ugr.es;User ID=x8768206;Password=x8768206')

        conn.autocommit = False
        cursor = conn.cursor()
        
    except Exception as ex:
        print(ex)
        
    return conn

conn = conectaBase()

###################################################################################################################################
def ventanaGestionClientes():
    newWindow = Toplevel()
    newWindow.config(width = "1080", height = "720", bd = "10", relief = "sunken")

    etiquetaInformacion = Label(newWindow, 
    font = ("Time News Roman", 10), text = "Gestión de Clientes.Por favor indique la gestion a realizar.")
    etiquetaInformacion.place(x = 300, y = 0)

    botonAnadirCliente = Button(newWindow, text = "1. Añadir un nuevo cliente", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10), command = anadirClienteInterfaz).place(x = 450, y = 50)

    botonBorrarCliente = Button(newWindow, text = "2. Borrar un cliente", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10)).place(x = 450, y = 100)

    botonModificarCliente = Button(newWindow, text = "3. Modificar datos de un cliente", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10)).place(x = 450, y = 150)

    botonGestionarSuscripcion = Button(newWindow, text = "4. Gestionar la suscripción de un cliente'", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10)).place(x = 450, y = 200)

    botonApuntarCliente = Button(newWindow, text = "5. Apuntar un cliente a una clase", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10)).place(x = 450, y = 250)

    botonMostrarClientes = Button(newWindow, text = "6. Mostrar datos de los clientes", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10)).place(x = 450, y = 300)

    botonMostrarClasesDeCliente = Button(newWindow, text = "7. Mostrar clases de un cliente", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10)).place(x = 450, y = 350)

    botonSalir = Button(newWindow, text = "8. Volver al menú principal", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10)).place(x = 450, y = 400)


camposCliente = ["DNI", "Nombre", "Apellidos", "Correo", "Dirección", "Telefono", "Tipo de Suscripción"]
datosCliente = ["", "", "", "", "", "", ""]

def anadirClienteInterfaz():
    newWindow = Toplevel()
    newWindow.config(width = "1080", height = "720", bd = "10", relief = "sunken")
    etiquetaInformacion = Label(newWindow, 
    font = ("Time News Roman", 10), text = "Introduzca los datos del cliente.")
    etiquetaInformacion.place(x = 300, y = 0)

    variables = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]

    for i in range(0, len(camposCliente)):
        label = Label(newWindow, text = camposCliente[i], font = ("Time News Roman", 10)).grid(row = i, column = 0, padx = 10, pady = 10)
        entry = Entry(newWindow, textvariable = variables[i])
        entry.grid(row = i, column = 1)
        
    boton = Button(newWindow, text = "Crear Usuario", command = lambda: getDato(variables))
    boton.grid(row = 7, column = 0, padx = 10, pady = 10)

    

        
    #dni = StringVar(newWindow)
    #entry = Text(newWindow)
    #
    # entry.place(x = 50, y = 50, width = "200", height = "20")
    #btn = Button(newWindow, command = lambda: prueba(entry)).place(x = 50, y = 150)
    
def getDato(dato):
    for i in range(0, len(camposCliente)):
        result = dato[i].get()
        datosCliente[i] = result
    
    clientes.anadirCliente(conn, datosCliente)
        #print(datosCliente[i])
        
###################################################################################################################################
miFrame = Frame()
miFrame.pack(expand = "True", fill = "both")
miFrame.config(width = "1080", height = "720", bd = "10", relief = "sunken")

etiquetaInformacion = Label(miFrame, 
font = ("Time News Roman", 10), text = "Bienvenido al centro deportivo Epicardo, por favor, eliga una de las siguientes opciones:")
etiquetaInformacion.place(x = 300, y = 0)

botonInicializar = Button(miFrame, text = "1. Inicializar BBDD", width = "30", 
cursor = "pirate", font = ("Time News Roman", 10), command = ini.main(conn)).place(x = 450, y = 50)

botonClientes = Button(miFrame, text = "2. Gestión de clientes", width = "30", 
cursor = "pirate", font = ("Time News Roman", 10), command = ventanaGestionClientes).place(x = 450, y = 150)

botonEntrenadores = Button(miFrame, text = "3. Gestión de entrenadores", width = "30", 
cursor = "pirate", font = ("Time News Roman", 10)).place(x = 450, y = 250)

botonClases = Button(miFrame, text = "4. Gestión de clases", width = "30", 
cursor = "pirate", font = ("Time News Roman", 10)).place(x = 450, y = 350)

botonInstalaciones = Button(miFrame, text = "5. Gestión de instalaciones", width = "30", 
cursor = "pirate", font = ("Time News Roman", 10)).place(x = 450, y = 450)

botonSalir = Button(miFrame, text = "6. Salir", width = "30", 
cursor = "pirate", font = ("Time News Roman", 10), command = raiz.destroy).place(x = 450, y = 550)

raiz.mainloop()