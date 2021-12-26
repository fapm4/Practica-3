import tkinter
from tkinter import *
from typing import NewType
import main as main
import inicializa as ini
import subsistema_clientes as clientes
import pyodbc


def ventanaGestionClientes():
    newWindow = Toplevel()
    newWindow.config(width = "1080", height = "720", bd = "10", relief = "sunken")

    etiquetaInformacion = Label(newWindow, 
    font = ("Time News Roman", 10), text = "Gestión de Clientes.Por favor indique la gestion a realizar.")
    etiquetaInformacion.place(x = 300, y = 0)

    botonAnadirCliente = Button(newWindow, text = "1. Añadir un nuevo cliente", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10), command = anadirClienteInterfaz).place(x = 450, y = 50)

    botonBorrarCliente = Button(newWindow, text = "2. Borrar un cliente", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10), command = borrarClienteInterfaz).place(x = 450, y = 100)

    botonModificarCliente = Button(newWindow, text = "3. Modificar datos de un cliente", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10), command = modificarClienteInterfaz).place(x = 450, y = 150)

    botonGestionarSuscripcion = Button(newWindow, text = "4. Gestionar la suscripción de un cliente", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10), command = modificarSuscripcionInterfaz).place(x = 450, y = 200)

    botonApuntarCliente = Button(newWindow, text = "5. Apuntar un cliente a una clase", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10), command = apuntarClienteInterfaz).place(x = 450, y = 250)

    botonSalir = Button(newWindow, text = "6. Volver al menú principal", width = "30", 
    cursor = "pirate", font = ("Time News Roman", 10), command = newWindow.destroy).place(x = 450, y = 300)


conn = main.conectaBase()

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
        
    botonCrear = Button(newWindow, text = "Crear Usuario", command = lambda: ejecutaAnadir(variables))
    botonCrear.grid(row = 7, column = 0, padx = 10, pady = 10)

    botonSalir = Button(newWindow, text = "Volver", command = newWindow.destroy)
    botonSalir.grid(row = 7, column = 1, padx = 10, pady = 10)
    
def ejecutaAnadir(dato):
    for i in range(0, len(camposCliente)):
        result = dato[i].get()
        datosCliente[i] = result
    
    clientes.anadirCliente(conn, datosCliente)

def borrarClienteInterfaz():
    newWindow = Toplevel()
    newWindow.config(width = "1080", height = "720", bd = "10", relief = "sunken")
    etiquetaInformacion = Label(newWindow, 
    font = ("Time News Roman", 10), text = "Introduzca los datos del cliente.")
    etiquetaInformacion.place(x = 300, y = 0)

    dniCliente = StringVar()
    label = Label(newWindow, text = camposCliente[0], font = ("Time News Roman", 10)).grid(row = 0, column = 0, padx = 10, pady = 10)
    entry = Entry(newWindow, textvariable = dniCliente)
    entry.grid(row = 0, column = 1)
        
    botonCrear = Button(newWindow, text = "Borrar Usuario", command = lambda: ejecutaBorrar(dniCliente))
    botonCrear.grid(row = 7, column = 0, padx = 10, pady = 10)

    botonSalir = Button(newWindow, text = "Volver", command = newWindow.destroy)
    botonSalir.grid(row = 7, column = 1, padx = 10, pady = 10)
        
def ejecutaBorrar(dato):
    result = dato.get()
    clientes.borrarCliente(conn, result)

def modificarClienteInterfaz():
    newWindow = Toplevel()
    newWindow.config(width = "1080", height = "720", bd = "10", relief = "sunken")
    etiquetaInformacion = Label(newWindow, 
    font = ("Time News Roman", 10), text = "Introduzca los datos del cliente.")
    etiquetaInformacion.place(x = 300, y = 0)

    variables = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]

    for i in range(0, len(camposCliente)):

        if i == 6:
            label = Label(newWindow, text = "Nuevo dni", font = ("Time News Roman", 10)).grid(row = i, column = 0, padx = 10, pady = 10)
        else:
            label = Label(newWindow, text = camposCliente[i], font = ("Time News Roman", 10)).grid(row = i, column = 0, padx = 10, pady = 10)
        entry = Entry(newWindow, textvariable = variables[i])
        entry.grid(row = i, column = 1)
        
    botonCrear = Button(newWindow, text = "Modificar Usuario", command = lambda: ejecutaModificar(variables))
    botonCrear.grid(row = 7, column = 0, padx = 10, pady = 10)

    botonSalir = Button(newWindow, text = "Volver", command = newWindow.destroy)
    botonSalir.grid(row = 7, column = 1, padx = 10, pady = 10)

def ejecutaModificar(dato):
    for i in range(0, len(camposCliente)):
        result = dato[i].get()
        datosCliente[i] = result
    
    clientes.modificarCliente(conn, datosCliente)

def modificarSuscripcionInterfaz():
    newWindow = Toplevel()
    newWindow.config(width = "1080", height = "720", bd = "10", relief = "sunken")
    etiquetaInformacion = Label(newWindow, 
    font = ("Time News Roman", 10), text = "Introduzca los datos del cliente.")
    etiquetaInformacion.place(x = 300, y = 0)

    dniCliente = StringVar()
    label = Label(newWindow, text = camposCliente[0], font = ("Time News Roman", 10)).grid(row = 0, column = 0, padx = 10, pady = 10)
    entry = Entry(newWindow, textvariable = dniCliente)
    entry.grid(row = 0, column = 1)

    suscripcionCliente = StringVar()
    label = Label(newWindow, text = camposCliente[6], font = ("Time News Roman", 10)).grid(row = 1, column = 0, padx = 10, pady = 10)
    entry = Entry(newWindow, textvariable = suscripcionCliente)
    entry.grid(row = 1, column = 1)

        
    botonCrear = Button(newWindow, text = "Modificar suscripción", command = lambda: ejecutaModSuscripcion(dniCliente, suscripcionCliente))
    botonCrear.grid(row = 7, column = 0, padx = 10, pady = 10)

    botonSalir = Button(newWindow, text = "Volver", command = newWindow.destroy)
    botonSalir.grid(row = 7, column = 1, padx = 10, pady = 10)

def ejecutaModSuscripcion(dniC, susC):
    dni = dniC.get()
    sus = susC.get()
    clientes.gestionarSuscripcion(conn, dni, sus)

def apuntarClienteInterfaz():
    newWindow = Toplevel()
    newWindow.config(width = "1080", height = "720", bd = "10", relief = "sunken")
    etiquetaInformacion = Label(newWindow, 
    font = ("Time News Roman", 10), text = "Introduzca los datos del cliente.")
    etiquetaInformacion.place(x = 300, y = 0)

    dniCliente = StringVar()
    label = Label(newWindow, text = camposCliente[0], font = ("Time News Roman", 10)).grid(row = 0, column = 0, padx = 10, pady = 10)
    entry = Entry(newWindow, textvariable = dniCliente)
    entry.grid(row = 0, column = 1)

    idClase = StringVar()
    label = Label(newWindow, text = "ID de la clase", font = ("Time News Roman", 10)).grid(row = 1, column = 0, padx = 10, pady = 10)
    entry = Entry(newWindow, textvariable = idClase)
    entry.grid(row = 1, column = 1)

        
    botonCrear = Button(newWindow, text = "Apuntar a clase", command = lambda: ejecutaApuntar(dniCliente, idClase))
    botonCrear.grid(row = 7, column = 0, padx = 10, pady = 10)

    botonSalir = Button(newWindow, text = "Volver", command = newWindow.destroy)
    botonSalir.grid(row = 7, column = 1, padx = 10, pady = 10)

def ejecutaApuntar(dniC, idC):
    dni = dniC.get()
    id = idC.get()

    clientes.apuntarAClase(conn, dni, id)
