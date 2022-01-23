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
        print("3. Reservar una pista ")
        print("4. Cancelar una reserva")
        print("5. Mostrar reservas de una instalacion en un dia")
        print("6. Consultar reserva")
        print("7. Salir.")

        opcion =int(input("\nElija una opción: \n"))
        os.system('cls' if os.name == 'nt' else 'clear')
        if(opcion == 1):
            registrar_instalacion(conn)
        elif(opcion == 2):
            mostrar_instalacion(conn)
        elif(opcion==3):
            reservar_instalacion(conn)
        elif(opcion==4):
            cancelar_reserva(conn)
        elif(opcion==5):
            mostrar_horario(conn)
        elif(opcion==6):
            consultar_reserva(conn)


def reservar_instalacion(conn):
    cursor = conn.cursor()
    id = max_id(conn)
    id+=1

    n_inst = input("Introduce el id de la instalacion: ")
    dni = input("Introduce el dni: ")
    dia =(input("Introduce el día en el que tentrá lugar la reserva(YYYY/MM/DD): "))
    hora = (input("Introduce la hora a la que tendrá lugar la reserva(HH24:MI): "))

    f = "TO_DATE('" + str(dia) + str(hora) + "/"+ ":00','YYYY/MM/DD HH24:MI')"

    cursor.execute("SELECT * FROM RESERVA WHERE id_instalacion= %s")%(n_inst)
    lista=cursor.fetchall()
    existe = True
    for row in lista:
        if(row[2]==fecha):
            existe=False
            break
    if(existe):
        consulta = "INSERT INTO RESERVA (id_instalacion,dni,fecha) values (%s,%s,%s)"%(n_inst,dni,f)
    else:
        print("Ya hay una reserva a esa hora")

    try:
        cursor.execute(consulta)
        cursor.commit()
    except Exception as ex:
        print(ex)
        cursor.rollback()

def cancelar_reserva(conn):
    mid = max_id(conn)
    cursor = conn.cursor()

    if(mid != -1):
        try:
            i = int(input("Introduzca el id de la reserva a cancelar.\n-1 para borrar todas la reservas: "))
            if(i == -1):
                consulta ="DELETE FROM INSTALACION"
                try:
                    cursor.execute(consulta)
                    cursor.commit()

                except Exception as ex:
                    print(ex)
                    cursor.rollback()
            elif(-1 <= i <=mid):
                consulta = "DELETE FROM INSTALACION WHERE id_clase='%s'"%(i)

                try:
                    cursor.execute(consulta)
                    cursor.commit()

                except Exception as ex:
                    print(ex)
                    cursor.rollback()
            else:
                print("\nIntroduzca un identificador correcto.\n")
        except:
            print("Introduce un número, no una letra.")
    else:
        print("\nNo hay nada que borrar.\n")
    return

def mostrar_horario(conn):
    n_inst = input("Introduce el id de la instalación: ")
    print("\n")
    cursor = conn.cursor()
    consulta = "SELECT * FROM RESERVA"

    cursor.execute(consulta)
    lista = cursor.fetchall()
    if(len(lista) == 0):
        print("\nNo hay reservas.\n")
    else:
        msg = ("Pista %s")%(n_inst)
        for row in lista:
            if(row[1]==n_inst):
                msg += ("DNI: %s Fecha: %s ")%(row[0],row[2])
                print(msg)
                print("\n")

def consultar_reserva(conn):
    n_inst = input("Introduce el id de la instalación: ")
    print("\n")

    cursor = conn.cursor()
    consulta = "SELECT * FROM RESERVA"

    if(len(lista) == 0):
        print("\nNo hay reservas.\n")

    else:

        f = input("Intoduce la fecha de la reserva:")
        print("\n")

        for row in lista:
            if(row[1]==n_inst):
                if(row[2]==f):
                    msg += ("El cliente que ha reservado esta pista el dìa %s es: %s ")%(f,row[0])

                    print(msg)
                    print("\n")



    cursor.execute(consulta)
    lista = cursor.fetchall()
    return
