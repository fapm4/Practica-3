#!/usr/bin/env python
# coding: utf-8

# Practica 3

import pyodbc
from time import gmtime, strftime

# In[ ]:

def aniadeEntrenador(conn):
    try:
        print("\nIntroduzca el DNI del nuevo entrenador\n")
        dni_entrenador=str(input())
        print("Introduzca el nombre del nuevo entrenador\n")
        nombre_entrenador=str(input())
        print("Introduzca los apellidos del nuevo entrenador\n")
        apellidos_entrenador=str(input())
        print("Introduzca la direccion del nuevo entrenador\n")
        direccion_entrenador=str(input())
        print("Introduzca el correo del nuevo entrenador\n")
        correo_entrenador=str(input())
        print("Introduzca el telefono del nuevo entrenador\n")
        n_telefono=int(input())
        espe=15
        while espe > 3:
            print("Introduzca la especialidad del nuevo entrenador\n")
            print("1. Raqueta\n")
            print("2. Equipo\n")
            print("3. Personal\n")
            espe=int(input())
            if espe==1:
                especialidad="Raqueta"
            elif espe == 2:
                especialidad="Equipo"
            elif espe == 3:
                especialidad="Personal"

        with conn.cursor() as cursor: 
                new_entrenador =  """INSERT INTO ENTRENADORES (DNI, NOMBRE, APELLIDOS, CORREO, DIRECCION, TELEFONO, ESPECIALIDAD) VALUES ('%s','%s','%s','%s','%s',%s,'%s')"""%(dni_entrenador,nombre_entrenador,apellidos_entrenador,correo_entrenador,direccion_entrenador,n_telefono,especialidad)
                cursor.execute(new_entrenador)
                cursor.commit()

    except Exception as ex:
            print(ex)
            
            with conn.cursor() as cursor:
                cursor.rollback()
    
    return conn

def existe_entrenador(conn, dni):
    try:
        consulta =  """SELECT * FROM ENTRENADORES WHERE DNI='%s'"""%(dni)
        
        with conn.cursor() as cursor:           
            cursor.execute(consulta)
            existe = cursor.fetchall()

    except Exception as ex:
        print(ex)

    return existe

def borraEntrenador(conn):
    
    print("\nIntroduzca el DNI del entrenador que quiere borrar:\t")
    dni_entrenador=str(input())
    
    if not existe_entrenador(conn, dni_entrenador):
        print("\nEl entrenador con el DNI pasado no existe en la base de datos\n")
    else:
        try:
            delete_entrenador =  """DELETE FROM ENTRENADORES WHERE DNI='%s'"""%(dni_entrenador)
            
            with conn.cursor() as cursor:           
                cursor.execute(delete_entrenador)
                cursor.commit()

        except Exception as ex:
            print(ex)

            with conn.cursor() as cursor:
                cursor.rollback()

    return conn

def horario(conn):

    print("\nIntroduzca el DNI del entrenador del que quiere saber el horario:\t")
    dni_entrenador=str(input())

    if not existe_entrenador(conn, dni_entrenador):
        print("\nEl entrenador con el DNI pasado no existe en la base de datos\n")
    else:
        try:
            horas = """ SELECT NOMBRE, APELLIDOS, HORARIO FROM ENTRENADORES, IMPARTE, CLASE WHERE DNI='%s' """%(dni_entrenador)
            
            with conn.cursor() as cursor:
                cursor.execute(horas)
                horario = cursor.fetchall() 

        except Exception as ex:
            print(ex)

    return conn

def muestraEntrenadores(conn):
    try:
        consulta =  "SELECT DNI,NOMBRE,APELLIDOS,ESPECIALIDAD FROM ENTRENADORES"

        with conn.cursor() as cursor:           
            cursor.execute(consulta)
            entrenadores = cursor.fetchall()

        if not entrenadores:
            print("\nLa base de datos no tiene ningun entrenador en este momento\n")
        else:
            for entrenador in entrenadores:
                un_entrenador="""\n\nDNI: %s\nEntrenador: %s %s\nEspecialidad: %s\n"""%(entrenador[0],entrenador[1],entrenador[2],entrenador[3])
                print(un_entrenador)

    except Exception as ex:
        print(ex)

    return conn

def gestionEntrenadores(conn):
    opcion=1

    while opcion > 0 and opcion < 6:
        print('Gestión de Entrenadores\nPor favor indique la gestion a realizar\n')
        print('1. Añadir un nuevo entrenador\n')
        print('2. Borrar un entrenador\n')
        print('3. Calcular el salario de un entrenador\n')
        print('4. Consultar el horario de un entrenador\n')
        print('5. Listado de todos los entrenadores\n')
        print('6. Salir\n')
        print('Introduce opción: ')

        opcion=int(input())

        if opcion==1:
            aniadeEntrenador(conn)
        elif opcion==2:
            borraEntrenador(conn)
        elif opcion==3:
            print("\nEsta función aún no está implementada\n")
        elif opcion==4:
            print("\nEsta función aún no está implementada\n")
        elif opcion==5:
            muestraEntrenadores(conn)


    return conn
     