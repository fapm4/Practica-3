#!/usr/bin/env python
# coding: utf-8

# Practica 3

# In[ ]:

import pyodbc
from time import gmtime, strftime

def conectaBase():
    try:
        conn = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0.ugr.es;Service Name=practbd.oracle0.ugr.es;User ID=x8768206;Password=x8768206')
        
    except Exception as ex:
        print(ex)
        
    return conn

def createTables(conn):

    try:
        createClase = ''' CREATE TABLE CLASE( 
            id_clase VARCHAR2(9),
            tematica VARCHAR2(40), 
            horario  DATE, 
            CONSTRAINT PK_CLASE PRIMARY KEY(id_clase))'''

        with conn.cursor() as cursor: 
            cursor.execute(createClase)

        createEntrenadores = ''' CREATE TABLE ENTRENADORES(
            DNI VARCHAR2(9),
            NOMBRE VARCHAR2(40),
            APELLIDOS VARCHAR2(40),
            CORREO VARCHAR2(40),
            DIRECCION VARCHAR2(40),
            TELEFONO NUMBER,
            ESPECIALIDAD VARCHAR2(40) CHECK (ESPECIALIDAD='Raqueta' OR ESPECIALIDAD='Equipo' OR ESPECIALIDAD='Personal') ,
            SALARIO NUMBER,
            CONSTRAINT PK_CLIENTES PRIMARY KEY (DNI),
            CONSTRAINT UK_CLIENTES_CORREO UNIQUE (CORREO),
            CONSTRAINT UK_CLIENTES_TELEFONO UNIQUE (TELEFONO))'''

        with conn.cursor() as cursor: 
            cursor.execute(createEntrenadores)

        createClientes = ''' CREATE TABLE CLIENTES(
            DNI VARCHAR2(9),
            NOMBRE VARCHAR2(40),
            APELLIDOS VARCHAR2(40),
            CORREO VARCHAR2(40),
            DIRECCION VARCHAR2(40),
            TELEFONO NUMBER(9),
            TIPO_SUSCRIPCION VARCHAR2(2),
            CONSTRAINT PPK_CLIENTES PRIMARY KEY (DNI),
            CONSTRAINT PUK_CLIENTES_CORREO UNIQUE (CORREO),
            CONSTRAINT PUK_CLIENTES_TELEFONO UNIQUE (TELEFONO))'''

        with conn.cursor() as cursor: 
            cursor.execute(createClientes)

        createInstalacion = ''' CREATE TABLE INSTALACION(
            id_instalacion VARCHAR2(9),
            aforo NUMBER,
            CONSTRAINT IPK_CLASE PRIMARY KEY(id_instalacion))'''

        with conn.cursor() as cursor: 
            cursor.execute(createInstalacion)

        createReserva = ''' CREATE TABLE RESERVA(
            DNI VARCHAR2(9),
            ID_INSTALACION VARCHAR2(9),
            FECHA DATE,
            CONSTRAINT PK_RESERVA PRIMARY KEY(DNI),
            CONSTRAINT FK_RESERVA_INSTALACION FOREIGN KEY(ID_INSTALACION) REFERENCES INSTALACION)'''

        with conn.cursor() as cursor: 
            cursor.execute(createReserva)
        
        createApuntado = ''' CREATE TABLE APUNTADO(
            DNI VARCHAR2(9),
            ID_CLASE VARCHAR2(9),
            CONSTRAINT PK_APUNTADO PRIMARY KEY(DNI),
            CONSTRAINT FK_APUNTADO_CLASE FOREIGN KEY(ID_CLASE) REFERENCES CLASE)'''

        with conn.cursor() as cursor: 
            cursor.execute(createApuntado)

        createImparte = ''' CREATE TABLE IMPARTE(
            DNI VARCHAR2(9),
            id_clase VARCHAR2(9),
            CONSTRAINT EK_CLASEI FOREIGN KEY (id_clase) REFERENCES CLASE,
            CONSTRAINT EK_DNI FOREIGN KEY (DNI) REFERENCES ENTRENADORES,
            CONSTRAINT PK_IMPARTE PRIMARY KEY(id_clase,DNI))'''

        with conn.cursor() as cursor: 
            cursor.execute(createImparte)

        createLugar = ''' CREATE TABLE LUGAR(
            id_instalacion VARCHAR2(9),
            id_clase VARCHAR2(9),
            CONSTRAINT EK_CLASEL FOREIGN KEY (id_clase) REFERENCES CLASE,
            CONSTRAINT EK_INSTALACION FOREIGN KEY (id_instalacion) REFERENCES INSTALACION,
            CONSTRAINT PK_LUGAR PRIMARY KEY(id_clase,id_instalacion))'''

        with conn.cursor() as cursor: 
            cursor.execute(createLugar)

    except Exception as ex:
        print(ex)

def dropBD(conn):
    tablas=["LUGAR", "IMPARTE", "APUNTADO", "RESERVA", "INSTALACION", "CLIENTES", "ENTRENADORES", "CLASE"]
    i=0
    while i < 8:        
        try:
            vaciado = "DROP TABLE " + tablas[i]

            with conn.cursor() as cursor:
                cursor.execute(vaciado)

        except Exception as ex:
            print(ex)
            
            with conn.cursor() as cursor:
                cursor.rollback()
        i+=1

def gestionEntrenadores(conn):
    caca = "hola"

#########################################################################################################################3
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

def pedirDatosCliente(nuevo):

    print("Nombre: ")
    nombre = str(input())

    print("Apellidos: ")
    apellidos = str(input())

    print("Correo: ")
    correo = str(input())

    print("Dirección: ")
    direccion = str(input())

    print("Teléfono: ")
    telefono = int(input())

    if nuevo:
        print("Tipo de suscripcion: ")
        suscripcion = str(input())

    else:
        suscripcion = ""
    return nombre, apellidos, correo, direccion, telefono, suscripcion

def anadirCliente(conn):

    print("DNI: ")
    dniCliente = str(input())

    # Vamos a buscar primero al cliente por su DNI en la tabla de CLIENTE
    # Se tiene que cambiar por un trigger

    if buscaCliente(conn, dniCliente) == 0:
        print("El cliente ya existe")
    else:

        nombreCliente, apellidosCliente, correoCliente, direccionCliente, telefonoCliente, suscripcionCliente = pedirDatosCliente(True)
        
        insertaCliente = """
            INSERT INTO CLIENTES 
            (DNI, NOMBRE, APELLIDOS, CORREO, DIRECCION, TELEFONO, TIPO_SUSCRIPCION) 
            values ('%s', '%s', '%s', '%s', '%s', %i, '%s')
        """%(dniCliente, nombreCliente, apellidosCliente, correoCliente,
            direccionCliente, telefonoCliente, suscripcionCliente)
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
        sentencia = "DELETE FROM CLIENTES WHERE DNI = '" + dniCliente + "'";
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

    if buscaCliente(conn, dniCliente) == 0:
        nombreCliente, apellidosCliente, correoCliente, direccionCliente, telefonoCliente, suscripcionCliente = pedirDatosCliente(False)
        sentencia = "UPDATE CLIENTES SET TELEFONO = " + str(telefonoCliente) + ", NOMBRE = \'" + nombreCliente + "\', APELLIDOS = \'" + apellidosCliente + "\', CORREO = \'" + correoCliente + "\', DIRECCION = \'" + direccionCliente + "\' WHERE DNI = \'" + dniCliente + "\';"; 
        print(sentencia)
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
        sentencia = "UPDATE CLIENTES SET TIPO_SUSCRIPCION = \'" + tipoSuscripcion + "\' WHERE DNI = \'" + dniCliente + "\';"; 
        print(sentencia)
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
    print("#########################################################################")
    val = 1
    while(val >= 1 and val <= 4) and val != 7:
        print('Gestión de Clientes\nPor favor indique la gestion a realizar\n')
        print('1. Añadir un nuevo cliente\n')
        print('2. Borrar un cliente\n')
        print('3. Modificar datos de un cliente\n')
        print('4. Gestionar la suscripción de un cliente\n')
        print('5. Apuntar un cliente a una clase\n')
        print('6. Mostrar datos de los clientes\n')
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


def main():
    conn = conectaBase()

    print("Bienvenido al Centro Deportivo Epicardo.\nIndica a continuación una de las opciones.")
    print('\n')
    
    val = 1

    while (val >= 0 and val <= 4) and val != 5:
        print('0. Inicializar la base de datos\n')
        print('1. Gestión de Clientes\n')
        print('2. Gestión de Entrenadores\n')
        print('3. Gestión de Clases\n')
        print('4. Gestión de Instalaciones\n')
        print('5. Salir (sin confirmar cambios)\n')
        print('Introduce opción: ')
        val = int(input())
        
        if val != 5:
            if val == 0:
                dropBD(conn)
                createTables(conn)
            elif val == 1:
                gestionClientes(conn)
            elif val == 2:
                gestionEntrenadores(conn)
            elif val == 3:
                print('Esta parte es de Jose\n')
            elif val == 4:
                print('Esta parte es de Fjorn\n')
        else:
            with conn.cursor() as cursor:
                cursor.rollback()

    conn.close()

main()
