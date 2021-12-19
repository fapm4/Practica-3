#!/usr/bin/env python
# coding: utf-8

# Practica 3

# In[ ]:

import pyodbc
import os
import inicializa
from time import gmtime, strftime


##########################################################################################################################
def buscaCliente(conn, cli):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DNI FROM CLIENTES")
    
            existe = -1
            
            # Los recupero y los guardo
            dataClientes = cursor.fetchall()

            if len(dataClientes) != 0:
                for prod in dataClientes:
                    #print(prod[0])
                    if cli is prod[0] or cli == prod[0]:
                        existe = 0   
                
    except Exception as ex:
        print(ex)
        
    return existe


def campoVacio(campo):
    if campo == "":
        return True
    else:
        return False

def pedirDatosCliente(nuevo):

    campos = ["Nombre", "Apellidos", "Correo", "Dirección", "Telefono", "Tipo de Suscripción"]
    val = ["", "", "", "", "", ""]

    if nuevo:
        p = 6
    else:
        p = 5

    for i in range(0, p):

        aux = ""
        while(campoVacio(aux)):

            aux = str(input(campos[i] + ": "))

            if campoVacio(aux):
                print("No se admiten campos vacios.\nPor favor introduzca el campo %s con el dato correspondiente"%(campos[i]))
        
            else:
                val[i] = aux
    return val

def convierteTelefono(telefonoCliente):
    try:
        toDev = int(telefonoCliente)
    except Exception as ex:
        if isinstance(ex, ValueError):
            #print("Ha introducido una letra en el teléfono - Carácter erróneo")
            toDev = -1

    return toDev

def muestraExcepcion(ex):
    errorCorreo = 'CONTROL_CORREO'
    errorTelefonoCaracter = 'CONTROL_TELEFONO'
    errorSuscripcion = 'CK_CLIENTES'
    errorTelefonoRepetido = 'UK_CLIENTES_TELEFONO'
    errorCorreoRepetido = 'UK_CLIENTES_CORREO'
    errorUpdateSuscripcion = 'CONTROL_SUSCRIPCION'
    errorFormatoDNI = 'CONTROL_DNI'
    errorLongitudTel = 'CONTROL_LONGITUD_TELEFONO'

    tipoError = ['CONTROL_CORREO', 'CONTROL_TELEFONO', 'CK_CLIENTES', 'UK_CLIENTES_TELEFONO', 'UK_CLIENTES_CORREO',
    'CONTROL_SUSCRIPCION', 'CONTROL_DNI', 'CONTROL_LONGITUD_TELEFONO']

    mensajeError = [
        "El formato del correo no sigue el formato _@_._",
        "Se ha introducido un carácter alfabético en el teléfono",
        "Tipo de suscripción no válida",
        "Telefono repetido",
        "Correo repetido",
        "Tipo de suscripción no válida",
        "Formato de DNI incorrecto",
        "Formato de teléfono invalido"
    ]

    print('----------------------------------------------')
    for i in range(0, 7):
        if tipoError[i] in str(ex):
            print(mensajeError[i])
    print('----------------------------------------------')
   

def anadirCliente(conn):

    dniCliente = ""
    while(dniCliente == ""):
        dniCliente = str(input("DNI: "))
        if campoVacio(dniCliente):
            print("No se admiten campos vacios, por favor introduzca el valor del DNI correspondiente")

    # Vamos a buscar primero al cliente por su DNI en la tabla de CLIENTE
    # Se tiene que cambiar por un trigger

    if buscaCliente(conn, dniCliente) == 0:
        print("El cliente ya existe")
    else:

        (nombreCliente, apellidosCliente, correoCliente, direccionCliente, telefonoCliente, suscripcionCliente) = pedirDatosCliente(True)
        tel = convierteTelefono(telefonoCliente)
        insertaCliente = """
            INSERT INTO CLIENTES 
            (DNI, NOMBRE, APELLIDOS, CORREO, DIRECCION, TELEFONO, TIPO_SUSCRIPCION) 
            values ('%s', '%s', '%s', '%s', '%s', %i, '%s')
        """%(dniCliente, nombreCliente, apellidosCliente, correoCliente,
            direccionCliente, tel, suscripcionCliente)

        #print(insertaCliente)
        try:
            with conn.cursor() as cursor:
                cursor.execute(insertaCliente)
                print(insertaCliente)
                cursor.commit()
        except Exception as ex:
            muestraExcepcion(ex)

            

def borrarCliente(conn):
    dniCliente = str(input("DNI: "))

    # Vamos a buscar primero al cliente por su DNI en la tabla de CLIENTE
    # Se tiene que cambiar por un trigger

    if buscaCliente(conn, dniCliente) == 0:
        sentencia = """
        DELETE FROM CLIENTES WHERE DNI = '%s'
        """%(dniCliente);
        try:
            with conn.cursor() as cursor:
                cursor.execute(sentencia)
                cursor.commit()
        except Exception as ex:
            print(ex)
    else:
        print("El cliente no existe")

def modificarCliente(conn):

    dniCliente = str(input("DNI: "))

    # Trigger

    if buscaCliente(conn, dniCliente) == 0:
        nombreCliente, apellidosCliente, correoCliente, direccionCliente, telefonoCliente, suscripcionCliente = pedirDatosCliente(False)
        tel = convierteTelefono(telefonoCliente)

        dniNuevo = str(input("DNI nuevo: "))
        sentencia = """
        UPDATE CLIENTES 
        SET TELEFONO = '%s', NOMBRE = '%s', APELLIDOS = '%s', 
        CORREO = '%s', DIRECCION = '%s', DNI = '%s' WHERE DNI = '%s';
        """%(tel, nombreCliente, apellidosCliente, correoCliente, direccionCliente, dniNuevo, dniCliente)
        
        #print(sentencia)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sentencia)
                cursor.commit()
        except Exception as ex:
            muestraExcepcion(ex)
    else:
        print("El cliente no existe")



def gestionarSuscripcion(conn):
    dniCliente = str(input("DNI: "))

    # Trigger y check sobre suscripcion
    if buscaCliente(conn, dniCliente) == 0:
        tipoSuscripcion = str(input("Introduce el nuevo tipo de suscripción: "))
        sentencia = """
        UPDATE CLIENTES SET TIPO_SUSCRIPCION = '%s' WHERE DNI = '%s';
        """%(tipoSuscripcion, dniCliente)
        #print(sentencia)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sentencia)
                cursor.commit()
        except Exception as ex:
            muestraExcepcion(ex)
    else:
        print("El cliente no existe")


def apuntarAClase(conn):
    print("DNI: ")
    dniCliente = str(input())

    # Comprobar aforo clase con trigger
    # y número de clases
    if buscaCliente(conn, dniCliente) == 0:
        print("ID de la clase: ")
        idClase = str(input())
        # Buscar clase con trigger

        sentencia = "INSERT INTO APUNTADO VALUES (\'" + dniCliente + "\', \'" + idClase + "\');"
        print(sentencia)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sentencia)
                cursor.commit()
        except Exception as ex:
            print(ex)
    else:
        print("El cliente no existe")

def muestraClientes(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM CLIENTES")
            dataClientes = cursor.fetchall()
            if len(dataClientes) != 0:
                for prod in dataClientes:
                    print("DNI  NOMBRE  APELLIDOS  CORREO  DIRECCION  TELÉFONO SUSCRIPCION")
                    print("""%s, %s, %s, %s, %s, %s, %s"""%(prod[0], prod[1], prod[2], prod[3], prod[4], prod[5], prod[6]))

            else:
                print("No hay información de clientes aún")
            

    except Exception as ex:
        print(ex)


def gestionClientes(conn):
    val = 1
    while(val >= 1 and val <= 6) and val != 7:
        print('Gestión de Clientes\nPor favor indique la gestion a realizar\n')
        print('1. Añadir un nuevo cliente')
        print('2. Borrar un cliente')
        print('3. Modificar datos de un cliente')
        print('4. Gestionar la suscripción de un cliente')
        print('5. Apuntar un cliente a una clase')
        print('6. Mostrar datos de los clientes')
        print('7. Volver al menú principal')
        print('Introduce opción: ')
        val = int(input())

        os.system('cls' if os.name == 'nt' else 'clear')
        if val == 1:
            anadirCliente(conn)
        elif val == 2:
            borrarCliente(conn)
        elif val == 3:
            modificarCliente(conn)
        elif val == 4:
            gestionarSuscripcion(conn)
        elif val == 5:
            apuntarAClase(conn)
        elif val == 6:
            muestraClientes(conn)
##########################################################################################################################