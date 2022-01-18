#!/usr/bin/env python
# coding: utf-8

# Practica 3

# In[ ]:

import pyodbc
import os
import tkinter
from tkinter import *
import inicializa
from time import gmtime, strftime
import subsistema_clases


##########################################################################################################################
def buscaDato(conn, dato, tabla):
    try:
        with conn.cursor() as cursor:
            if tabla == "clientes":
                sentencia = "SELECT DNI FROM CLIENTES"
            elif tabla == "clases":
                sentencia = "SELECT ID_CLASE FROM CLASE"

            cursor.execute(sentencia)
    
            existe = -1
            
            # Los recupero y los guardo
            data = cursor.fetchall()

            if len(data) != 0:
                for prod in data:
                    #print(prod[0])
                    if dato is prod[0] or dato == prod[0]:
                        existe = 0   
                
    except Exception as ex:
        print(ex)
        conn.rollback()
        
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

    tipoError = ['CONTROL_CORREO', 
    'CONTROL_TELEFONO', 
    'CK_CLIENTES', 
    'UK_CLIENTES_TELEFONO', 
    'UK_CLIENTES_CORREO',
    'CONTROL_SUSCRIPCION', 
    'CONTROL_DNI', 
    'CONTROL_LONGITUD_TELEFONO', 
    'CONTROL_CLASES_APUNTADAS', 
    'PK_APUNTADO']

    mensajeError = [
        "El formato del correo no sigue el formato _@_._",
        "Se ha introducido un carácter alfabético en el teléfono",
        "Tipo de suscripción no válida",
        "Telefono repetido",
        "Correo repetido",
        "Tipo de suscripción no válida",
        "Formato de DNI incorrecto",
        "Formato de teléfono invalido",
        "Se ha alcanzado el máximo de clases por mes",
        "Cliente ya apuntado a esa clase"]

    stop = True
    print('----------------------------------------------')
    for i in range(0, len(mensajeError)):
        if tipoError[i] in str(ex):
            print(mensajeError[i])
            stop = False

    print('----------------------------------------------')
   
    if stop == True:
        print(ex)

def anadirCliente(conn, datos):

    if(len(datos) != 0):
        dniCliente = datos[0]
    else:
        dniCliente = ""

    while(dniCliente == ""):
        dniCliente = str(input("DNI: "))
        if campoVacio(dniCliente):
            print("No se admiten campos vacios, por favor introduzca el valor del DNI correspondiente")

    # Vamos a buscar primero al cliente por su DNI en la tabla de CLIENTE

    if buscaDato(conn, dniCliente, "clientes") == 0:
        print("El cliente ya existe")
        conn.rollback()
    else:
        if(len(datos) != 0):
            (dniCliente, nombreCliente, apellidosCliente, correoCliente, direccionCliente, telefonoCliente, suscripcionCliente) = datos
        else:
            (nombreCliente, apellidosCliente, correoCliente, direccionCliente, telefonoCliente, suscripcionCliente) = pedirDatosCliente(True)
            
        tel = convierteTelefono(telefonoCliente)
        
        insertaCliente = """
            INSERT INTO CLIENTES 
            (DNI, NOMBRE, APELLIDOS, CORREO, DIRECCION, TELEFONO, TIPO_SUSCRIPCION, CLASES_APUNTADAS) 
            VALUES ('%s', '%s', '%s', '%s', '%s', %i, '%s', %i)
        """%(dniCliente, nombreCliente, apellidosCliente, correoCliente,
            direccionCliente, tel, suscripcionCliente, 0)

        #print(insertaCliente)
        try:
            with conn.cursor() as cursor:
                cursor.execute(insertaCliente)
                print(insertaCliente)
                cursor.commit()

        except Exception as ex:
            muestraExcepcion(ex)
            conn.rollback()

def borrarCliente(conn, dato):

    if(dato != ""):
        dniCliente = dato

    else:
        dniCliente = str(input("DNI: "))


    # Vamos a buscar primero al cliente por su DNI en la tabla de CLIENTE

    if buscaDato(conn, dniCliente, "clientes") == 0:
        sentencia = """
        DELETE FROM CLIENTES WHERE DNI = '%s'
        """%(dniCliente);
        try:
            with conn.cursor() as cursor:
                cursor.execute(sentencia)
                cursor.commit()
        except Exception as ex:
            print(ex)
            conn.rollback()
    else:
        print("El cliente no existe")
        conn.rollback()

def modificarCliente(conn, datos):

    if(len(datos) != 0):
        dniCliente = datos[0]
    else:
        dniCliente = ""

    if buscaDato(conn, dniCliente, "clientes") == 0:

        if(len(datos) != 0):
            (dniCliente, nombreCliente, apellidosCliente, correoCliente, direccionCliente, telefonoCliente, dniNuevo) = datos

        else:
            nombreCliente, apellidosCliente, correoCliente, direccionCliente, telefonoCliente, suscripcionCliente = pedirDatosCliente(False)
            dniNuevo = str(input("DNI nuevo: "))

        tel = convierteTelefono(telefonoCliente)

        
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
            conn.rollback()
    else:
        print("El cliente no existe")
        conn.rollback()



def gestionarSuscripcion(conn, dni, sus):

    if(dni != "" and sus != ""):
        dniCliente = dni
    else:
        dniCliente = str(input("DNI: "))
    
    if buscaDato(conn, dniCliente, "clientes") == 0:
        if(dni != "" and sus != ""):
            tipoSuscripcion = sus
        else:
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
            conn.rollback()
    else:
        print("El cliente no existe")
        conn.rollback()


def obtenNumClases(conn, dniCliente):
    sentencia = """
    SELECT CLASES_APUNTADAS FROM CLIENTES WHERE DNI ='%s'
    """%(dniCliente)
    try:
        with conn.cursor() as cursor:
            cursor.execute(sentencia)
            clases = cursor.fetchone()[0]
            cursor.commit()


    except Exception as ex:
        print(ex)
        conn.rollback()

    return clases

def reiniciaClases(conn, dniCliente):
    sentencia = "SELECT CURRENT_DATE FROM DUAL"
    try:
        with conn.cursor() as cursor:
            cursor.execute(sentencia)

            fecha = cursor.fetchone()
            dia = fecha[0:2]
            if dia == "01":
                sentencia = """
                UPDATE CLIENTES SET 
                CLASES_APUNTADAS = 0 WHERE DNI = '%s'
                """%(dniCliente)
                
                with conn.cursor() as cursor:
                    cursor.execute(sentencia)
                    
    except Exception as ex:
        print(ex)
        conn.rollback()

def apuntarAClase(conn, dni, idclase):

    reiniciaClases(conn, dni)
    if(dni != ""):
        dniCliente = dni
    else:
        dniCliente = str(input("DNI: "))

    if buscaDato(conn, dniCliente, "clientes") == 0:

        if(idclase != ""):
            idClase = idclase
        else:
            subsistema_clases.mostrar_clases(conn)
            idClase = str(input("ID de la clase: "))
        
        # Busco la clase
        if buscaDato(conn, idClase, "clases") == 0:
            #print("Clase encontrada")

            # Primero miro el aforo de la clase
            sentencia = """
            SELECT AFORO FROM INSTALACION I, LUGAR L WHERE L.ID_CLASE = %i AND L.ID_INSTALACION = I.ID_INSTALACION
            AND L.ID_INSTALACION = (SELECT DISTINCT(I.ID_INSTALACION) 
            FROM INSTALACION I, LUGAR L WHERE L.ID_CLASE = %i AND L.ID_INSTALACION = I.ID_INSTALACION)
            """%(int(idClase), int(idClase))

            #print(sentencia)
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sentencia)
                    aforoMaximo = cursor.fetchone()[0]
            except Exception as ex:
                print(ex)
                conn.rollback()
    
            # Después busco en apuntados
            sentencia = """
            select count(DNI) from APUNTADO where ID_CLASE = %i;
            """%(int(idClase))

            try:
                with conn.cursor() as cursor:
                    cursor.execute(sentencia)
                    aforoActual = cursor.fetchone()[0]
            except Exception as ex:
                print(ex)
                conn.rollback()

            # Si queda espacio, meto al cliente
            if(aforoActual + 1 <= aforoMaximo):
                # Después miro el tipo de suscripcion y el número de clases mensual
                clases = obtenNumClases(conn, dniCliente)
                # Actualizo el número de clases
                sentencia = """
                UPDATE CLIENTES SET 
                CLASES_APUNTADAS = %i WHERE DNI = '%s'
                """%(clases + 1, dniCliente)

                try:
                    with conn.cursor() as cursor:
                        cursor.execute(sentencia)
                        # Me queda insertar en apuntado

                        sentencia = """
                        INSERT INTO APUNTADO VALUES('%s', %i)
                        """%(dniCliente, int(idClase))

                        cursor.execute(sentencia)
                        cursor.commit()

                except Exception as ex:
                    muestraExcepcion(ex)
                    conn.rollback()

            else:
                print("Aforo máximo completado")
                conn.rollback()
        else:
            print("No existe la clase")
            conn.rollback()
    else:
        print("El cliente no existe")
        conn.rollback()

def muestraClientes(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM CLIENTES")
            dataClientes = cursor.fetchall()
            if len(dataClientes) != 0:
                print("----------------------------------------")
                for prod in dataClientes:
                    print("#############################################")
                    print("DNI: %s"%(prod[0]))
                    print("Nombre: %s"%(prod[1]))
                    print("Apellidos: %s"%(prod[2]))
                    print("Correo: %s"%(prod[3]))
                    print("Dirección: %s"%(prod[4]))
                    print("Teléfono: %s"%(prod[5]))
                    print("Suscripción: %s"%(prod[6]))
                    print("#############################################")
            else:
                print("No hay información de clientes aún")
                print("----------------------------------------")
            

    except Exception as ex:
        print(ex)

def mostrarClasesDeCliente(conn):
    dniCliente = str(input("DNI: "))

    if buscaDato(conn, dniCliente, "clientes") == 0:
        
        sentencia = """
        SELECT C.ID_CLASE, TEMATICA, HORARIO, I.ID_INSTALACION, AFORO 
        FROM CLASE C, INSTALACION I, APUNTADO A, LUGAR L 
        WHERE DNI = '%s' AND A.DNI = '%s'
        AND A.ID_CLASE = C.ID_CLASE
        AND L.ID_CLASE = C.ID_CLASE;
        """%(dniCliente, dniCliente)

        try:
            with conn.cursor() as cursor:
                cursor.execute(sentencia)
                dataClientes = cursor.fetchall()
                if len(dataClientes) != 0:
                    print("----------------------------------------")
                    for prod in dataClientes:
                        print("#############################################")
                        print("ID de la clase: %s"%(prod[0]))
                        print("Temática: %s"%(prod[1]))
                        print("Horario: %s"%(prod[2]))
                        print("ID de la instalación: %s"%(prod[3]))
                        print("Aforo máximo: %s"%(prod[4]))
                        print("#############################################")
                else:
                    print("No hay información de clientes aún")
                    print("----------------------------------------")
        
        except Exception as ex:
            print(ex)
    else:
        print("El cliente no existe")

def gestionClientes(conn):
    val = 1
    while(val >= 1 and val <= 7) and val != 8:
        print('Gestión de Clientes\nPor favor indique la gestion a realizar\n')
        print('1. Añadir un nuevo cliente')
        print('2. Borrar un cliente')
        print('3. Modificar datos de un cliente')
        print('4. Gestionar la suscripción de un cliente')
        print('5. Apuntar un cliente a una clase')
        print('6. Mostrar datos de los clientes')
        print('7. Mostrar clases de un cliente')
        print('8. Volver al menú principal')
        print('Introduce opción: ')
        val = int(input())

        os.system('cls' if os.name == 'nt' else 'clear')
        if val == 1:
            anadirCliente(conn, [])
        elif val == 2:
            borrarCliente(conn, "")
        elif val == 3:
            modificarCliente(conn, [])
        elif val == 4:
            gestionarSuscripcion(conn, "", "")
        elif val == 5:
            apuntarAClase(conn, "", "")
        elif val == 6:
            muestraClientes(conn)
        elif val == 7:
            mostrarClasesDeCliente(conn)

        conn.commit()
##########################################################################################################################
