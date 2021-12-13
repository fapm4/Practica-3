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

    campos = ["Nombre: ", "Apellidos: ", "Correo: ", "Dirección: ", "Telefono: ", "Tipo de Suscripción: "]
    val = ["", "", "", "", "", ""]

    if nuevo:
        p = 6
    else:
        p = 5

    for i in range(0, p):
        print(campos[i])

        aux = ""
        while(campoVacio(aux)):
            aux = str(input())

            if campoVacio(aux):
                print("No se admiten campos vacios, por favor introduzca los datos correspondientes")
        
            else:
                val[i]= aux


    return val

def anadirCliente(conn):

    dniCliente = ""
    while(dniCliente == ""):
        print("DNI: ")
        dniCliente = str(input())
        if campoVacio(dniCliente):
            print("No se admiten campos vacios, por favor introduzca los datos correspondientes")

    # Vamos a buscar primero al cliente por su DNI en la tabla de CLIENTE
    # Se tiene que cambiar por un trigger

    if buscaCliente(conn, dniCliente) == 0:
        print("El cliente ya existe")
    else:

        (nombreCliente, apellidosCliente, correoCliente, direccionCliente, telefonoCliente, suscripcionCliente) = pedirDatosCliente(True)
        
        insertaCliente = """
            INSERT INTO CLIENTES 
            (DNI, NOMBRE, APELLIDOS, CORREO, DIRECCION, TELEFONO, TIPO_SUSCRIPCION) 
            values ('%s', '%s', '%s', '%s', '%s', %i, '%s')
        """%(dniCliente, nombreCliente, apellidosCliente, correoCliente,
            direccionCliente, int(telefonoCliente), suscripcionCliente)
        try:
            with conn.cursor() as cursor:
                cursor.execute(insertaCliente)
                print(insertaCliente)
                cursor.commit()
        except Exception as ex:
            print(ex)

def borrarCliente(conn):
    print("DNI: ")
    dniCliente = str(input())

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

    print("DNI: ")
    dniCliente = str(input())

    # Trigger

    if buscaCliente(conn, dniCliente) == 0:
        nombreCliente, apellidosCliente, correoCliente, direccionCliente, telefonoCliente, suscripcionCliente = pedirDatosCliente(False)
        sentencia = """
        UPDATE CLIENTES 
        SET TELEFONO = '%s', NOMBRE = '%s', APELLIDOS = '%s', 
        CORREO = '%s', DIRECCION = '%s' WHERE DNI = '%s';
        """%(nombreCliente, apellidosCliente, correoCliente, direccionCliente, telefonoCliente, dniCliente)
        
        #print(sentencia)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sentencia)
                cursor.commit()
        except Exception as ex:
            print(ex)
    else:
        print("El cliente no existe")



def gestionarSuscripcion(conn):
    print("DNI: ")
    dniCliente = str(input())

    # Trigger y check sobre suscripcion
    if buscaCliente(conn, dniCliente) == 0:
        print("Introduce el nuevo tipo de suscripción: ")
        tipoSuscripcion = str(input())
        sentencia = """
        UPDATE CLIENTES SET TIPO_SUSCRIPCION = '%s' WHERE DNI = '%s';
        """%(tipoSuscripcion, dniCliente)
        #print(sentencia)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sentencia)
                cursor.commit()
        except Exception as ex:
            print(ex)
    else:
        print("El cliente no existe")


def apuntarAClase(conn):
    print("DNI: ")
    dniCliente = str(input())

    # Comprobar aforo clase con trigger
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
                    print("DNI  NOMBRE  APELLIDOS  CORREO  DIRECCION  TELEFONO SUSCRIPCION")
                    print("""%s, %s, %s, %s, %s, %s, %s"""%(prod[0], prod[1], prod[2], prod[3], prod[4], prod[5], prod[6]))

            else:
                print("No hay información de clientes aún")
            

    except Exception as ex:
        print(ex)


def gestionClientes(conn):
    val = 1
    while(val >= 1 and val <= 6) and val != 7:
        print('Gestión de Clientes\nPor favor indique la gestion a realizar\n')
        print('1. Añadir un nuevo cliente\n')
        print('2. Borrar un cliente\n')
        print('3. Modificar datos de un c7liente\n')
        print('4. Gestionar la suscripción de un cliente\n')
        print('5. Apuntar un cliente a una clase\n')
        print('6. Mostrar datos de los clientes\n')
        print('7. Volver al menú principal\n')
        print('Introduce opción: ')
        val = int(input())

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