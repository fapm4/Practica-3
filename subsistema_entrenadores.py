#!/usr/bin/env python
# coding: utf-8

# Practica 3

import pyodbc

import os

from time import gmtime, strftime

# In[ ]:

def aniadeEntrenador(conn):
    try:
        print("\nIntroduzca el DNI del nuevo entrenador")
        dni_entrenador=str(input())

        while len(dni_entrenador) > 9:
            print("\nEl DNI no puede tener mas de 9 caracteres\nIntroduzca de nuevo el DNI del nuevo entrenador")
            dni_entrenador=str(input())

        print("Introduzca el nombre del nuevo entrenador")
        nombre_entrenador=str(input())

        while len(nombre_entrenador) > 20:
            print("\nEl nombre no puede tener mas de 20 caracteres\nIntroduzca de nuevo el nombre del nuevo entrenador")
            nombre_entrenador=str(input())

        print("Introduzca los apellidos del nuevo entrenador")
        apellidos_entrenador=str(input())

        while len(apellidos_entrenador) > 40:
            print("\nLos apellidos no pueden tener mas de 40 caracteres\nIntroduzca de nuevo los apellidos del nuevo entrenador")
            apellidos_entrenador=str(input())

        print("Introduzca la direccion del nuevo entrenador")
        direccion_entrenador=str(input())

        while len(direccion_entrenador) > 60:
            print("\nLa direccion no puede tener mas de 60 caracteres\nIntroduzca de nuevo la direccion del nuevo entrenador")
            direccion_entrenador=str(input())

        print("Introduzca el correo del nuevo entrenador")
        correo_entrenador=str(input())

        while len(correo_entrenador) > 60:
            print("\nEl correo no puede tener mas de 60 caracteres\nIntroduzca de nuevo el correo del nuevo entrenador")
            correo_entrenador=str(input())

        print("Introduzca el telefono del nuevo entrenador")
        n_telefono=int(input())

        espe=15
        while not (0 < espe < 4):
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

        os.system('cls' if os.name == 'nt' else 'clear')

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

def salario(conn):

    print("\nIntroduzca el DNI del entrenador del que quiere calcular el salario:\t")
    dni_entrenador=str(input())

    if not existe_entrenador(conn, dni_entrenador):
        print("\nEl entrenador con el DNI pasado no existe en la base de datos\n")
    else:
        try:
            consulta = """SELECT NOMBRE, APELLIDOS FROM ENTRENADORES WHERE DNI='%s'"""%(dni_entrenador)

            with conn.cursor() as cursor:
                cursor.execute(consulta)
                entrenador = cursor.fetchall() 

            clases = """SELECT * FROM IMPARTE WHERE DNI='%s'"""%(dni_entrenador)
            
            with conn.cursor() as cursor:
                cursor.execute(clases)
                horario = cursor.fetchall()                 

            salario=0

            if not horario:
                print("\nEl entrenador seleccionado no imparte ninguna clase\n\n")
            else:
                for hora in horario:
                    salario+=3
                
                print("""\n\nEl entrenador %s %s recibira un salario de %s bocadillos\n\n """%(entrenador[0][0], entrenador[0][1],str(salario)))

                try:
                    insertar = """ UPDATE ENTRENADORES SET SALARIO=%s WHERE DNI='%s' """%(salario,dni_entrenador)

                    with conn.cursor() as cursor:
                        cursor.execute(insertar)
                        cursor.commit()

                except Exception as ex:
                    print(ex)
                    
                    with conn.cursor() as cursor:
                        cursor.rollback()

        except Exception as ex:
            print(ex)

    return conn

def horario(conn):

    print("\nIntroduzca el DNI del entrenador del que quiere saber el horario:\t")
    dni_entrenador=str(input())

    if not existe_entrenador(conn, dni_entrenador):
        print("\nEl entrenador con el DNI pasado no existe en la base de datos\n")
    else:
        try:
            consulta = """SELECT NOMBRE, APELLIDOS FROM ENTRENADORES WHERE DNI='%s'"""%(dni_entrenador)

            with conn.cursor() as cursor:
                cursor.execute(consulta)
                entrenador = cursor.fetchall() 

            horas = """ SELECT TEMATICA, HORARIO FROM IMPARTE I JOIN CLASE C ON I.ID_CLASE = C.ID_CLASE WHERE I.DNI='%s' """%(dni_entrenador)
            
            with conn.cursor() as cursor:
                cursor.execute(horas)
                horario = cursor.fetchall()                 

            if not horario:
                print("\nEl entrenador seleccionado no imparte ninguna clase")
            else:
                print("""\n\nEntrenador: %s %s"""%(entrenador[0][0], entrenador[0][1]))
                for hora in horario:
                    print("""Clase: %s \t\t Hora: %s \n"""%(hora[0], str(hora[1])))

        except Exception as ex:
            print(ex)

    return conn

def muestraEntrenadores(conn):
    try:
        consulta = "SELECT DNI,NOMBRE,APELLIDOS,ESPECIALIDAD FROM ENTRENADORES"

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

    while opcion != 6:
        print('Gestión de Entrenadores\n\nPor favor indique la gestión a realizar\n')
        print('1. Añadir un nuevo entrenador\n')
        print('2. Borrar un entrenador\n')
        print('3. Calcular el salario de un entrenador\n')
        print('4. Consultar el horario de un entrenador\n')
        print('5. Listado de todos los entrenadores\n')
        print('6. Salir\n')
        print('Introduce opción: ')

        opcion=int(input())

        os.system('cls' if os.name == 'nt' else 'clear')
        if opcion==1:
            aniadeEntrenador(conn)
        elif opcion==2:
            borraEntrenador(conn)
        elif opcion==3:
            salario(conn)
        elif opcion==4:
            horario(conn)
        elif opcion==5:
            muestraEntrenadores(conn)


    return conn
     