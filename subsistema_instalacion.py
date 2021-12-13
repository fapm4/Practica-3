from datetime import date
# from subsistema_instalacion import muestraInstalacion
import pyodbc
import os


def max_id(conn):
    cursor = conn.cursor()
    cursor.execute("select id_instalacion from INSTALACION")
    lit = cursor.fetchall()

    if( len(lit) <= 0):
        id = -1
    else:
        id = int(lit[len(lit)-1][0])
    
    return id

def registrar_instalacion(conn):
    cursor = conn.cursor()
    id = max_id(conn)
    id+=1
    aforo = input("Introduce el aforo de la instalacion: ")

    consulta = "INSERT INTO INSTALACION (id_instalacion,aforo) values (%s,%s)"%(id,aforo)
    
    try:
        cursor.execute(consulta)
        cursor.commit()
    except Exception as ex:
        print(ex)
        cursor.rollback()



def mostrar_instalacion(conn):
    print("\n")
    cursor = conn.cursor()
    consulta = "SELECT * FROM INSTALACION"
    cursor.execute(consulta)
    lista = cursor.fetchall()
    if(len(lista) == 0):
        print("\nNo hay instalaciones disponibles.\n")
    else:
        for row in lista:
            msg = ("ID: %s Aforo: %s ")%(row[0],row[1])
            print(msg)
            print("\n")

def gestionInstalacion(conn):
    opcion = 0
    while 0<= opcion <=2:
        print("1. Registrar instalacion.")
        print("2. Mostrar instalaciones.")
        print("3. Salir.")

        opcion =int(input("\nElija una opción: \n"))
        os.system('cls' if os.name == 'nt' else 'clear')
        if(opcion == 1):
            registrar_instalacion(conn)
        elif(opcion == 2):
            mostrar_instalacion(conn)