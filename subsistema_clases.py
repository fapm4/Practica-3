from datetime import date
from subsistema_entrenadores import muestraEntrenadores
from subsistema_instalacion import mostrar_instalacion
from subsistema_entrenadores import existe_entrenador

# from subsistema_instalacion import muestraInstalacion
import pyodbc
import array
import os


def id_clases(conn):
    cursor = conn.cursor()
    cursor.execute("select id_clase from CLASE")
    lit = cursor.fetchall()
    id = []
    contador = 0
    for row in lit:
        id.append(int(row[0]))

    return id


def id_clases_con_instalacion(conn):
    cursor = conn.cursor()
    cursor.execute("select id_clase from LUGAR")
    lit = cursor.fetchall()
    id = []
    contador = 0
    for row in lit:
        id.append(int(row[0]))

    return id


def id_clases_con_entrenador(conn):
    cursor = conn.cursor()
    cursor.execute("select id_clase from IMPARTE")
    lit = cursor.fetchall()
    id = []
    contador = 0
    for row in lit:
        id.append(int(row[0]))

    return id


def max_idC(conn):
    cursor = conn.cursor()
    cursor.execute("select id_clase from CLASE")
    lit = cursor.fetchall()

    if(len(lit) <= 0):
        id = -1
    else:
        id = int(lit[len(lit)-1][0])

    return id


def max_idE(conn):
    cursor = conn.cursor()
    cursor.execute("select dni from ENTRENADORES")
    lit = cursor.fetchall()

    if(len(lit) <= 0):
        id = -1
    else:
        id = 0

    return id


def max_idI(conn):
    cursor = conn.cursor()
    cursor.execute("select id_instalacion from INSTALACION")
    lit = cursor.fetchall()

    if(len(lit) <= 0):
        id = -1
    else:
        id = int(lit[len(lit)-1][0])

    return id


def crear_clase(conn):
    cursor = conn.cursor()

    tematica = str(input("Introduce la temática de la clase: "))
    while(len(tematica) == 0):
        tematica = str(input("Introduce una tematica válida: "))

    fecha = date.today()

    while True:
        try:
            dia = int(input("Introduce el día en el que tendrá lugar la clase: "))

            if(dia >= date.today().day and dia <= 31):
                break
            else:
                print("Valor incorrecto.")
        except:
            print("Valor incorrecto.")

    while True:
        try:
            hora = int(
                input("Introduce la hora a la que tendrá lugar la clase: "))
            if(hora >= 0 and hora <= 23):
                break
            else:
                print("Valor incorrecto.")
        except:
            print("Valor incorrecto.")

    atributos = [tematica, dia, hora]

    id = max_idC(conn)
    id += 1

    f = "TO_DATE('" + str(fecha.year) + "/" + str(fecha.month) + "/" + \
        str(atributos[1]) + " " + str(atributos[2]) + \
        ":00','YYYY/MM/DD HH24:MI')"
    """
    v= "values ('" + str(id) +"','" + atributos[0] + "'," + f +"));"
    consulta = "INSERT INTO CLASE (id_clase,tematica,horario) " + v
    """
    consulta = "INSERT INTO CLASE (id_clase,tematica,horario)  values ('%s','%s',%s)" % (
        id, atributos[0], f)

    try:
        cursor.execute(consulta)
        cursor.commit()
    except Exception as ex:
        print(ex)
        cursor.rollback()


def borrar_clase(conn):
    mid = max_idC(conn)
    cursor = conn.cursor()

    n_id = id_clases(conn)
    mostrar_clases(conn)

    if(mid != -1):
        try:
            i = int(input(
                "Introduzca el id de la clase que quiera borrar.\n -1 para borrar todas la clases: "))
            sets = {i}

            if(i == -1):
                consulta = "DELETE FROM CLASE "
                try:
                    cursor.execute(consulta)
                    cursor.commit()

                except Exception as ex:
                    print(ex)
                    cursor.rollback()
            elif(sets.issubset(n_id)):
                consulta = "DELETE FROM CLASE WHERE id_clase='%s' " % (
                    i)

                try:
                    cursor.execute(consulta)
                    cursor.commit()

                except Exception as ex:
                    print(ex)
                    cursor.rollback()
            else:
                print("\nIntroduzca un identificador correcto.\n")
        except:
            print("\nIntroduce un número, no una letra.\n")
    else:
        print("\nNo hay nada que borrar.\n")


def mostrar_clases(conn):
    print("\n")
    cursor = conn.cursor()
    consulta = "SELECT * FROM CLASE"
    cursor.execute(consulta)
    lista = cursor.fetchall()
    if(len(lista) == 0):
        print("\nNo hay clases disponibles.\n")
    else:
        for row in lista:
            msg = ("ID: %s Temática: %s  Fecha: %s") % (row[0], row[1], row[2])
            print(msg)
            print("\n")


def mostrar_clases_sin_instalacion(conn):
    print("\n")
    n_id = id_clases_con_instalacion(conn)
    cursor = conn.cursor()
    consulta = "SELECT * FROM CLASE"
    cursor.execute(consulta)
    lista = cursor.fetchall()
    if(len(lista) == 0):
        print("\nNo hay clases disponibles.\n")
    else:
        for row in lista:
            cpm = []
            cpm.append(int(row[0]))
            if(not all(item in n_id for item in cpm)):
                msg = ("ID: %s Temática: %s  Fecha: %s") % (
                    row[0], row[1], row[2])
                print(msg)
                print("\n")


def mostrar_clases_sin_entrenador(conn):
    print("\n")
    n_id = id_clases_con_entrenador(conn)
    cursor = conn.cursor()
    consulta = "SELECT * FROM CLASE"
    cursor.execute(consulta)
    lista = cursor.fetchall()
    if(len(lista) == 0):
        print("\nNo hay entrenadores disponibles.\n")
    else:
        for row in lista:
            cpm = []
            cpm.append(int(row[0]))
            if(not all(item in n_id for item in cpm)):
                msg = ("ID: %s Temática: %s  Fecha: %s") % (
                    row[0], row[1], row[2])
                print(msg)
                print("\n")


def hayclases(conn):
    if (max_idC(conn) != -1):
        return True
    else:
        return False


def hayentrenador(conn):
    if (max_idE(conn) != -1):
        return True
    else:
        return False


def hayinstalacion(conn):
    if (max_idI(conn) != -1):
        return True
    else:
        return False


def hay_clases_sin_entrenador(conn):
    print("\n")
    n_id = id_clases_con_entrenador(conn)
    cursor = conn.cursor()
    consulta = "SELECT * FROM CLASE"
    cursor.execute(consulta)
    lista = cursor.fetchall()
    bul = False
    for row in lista:
        cpm = []
        cpm.append(int(row[0]))
        if(not all(item in n_id for item in cpm)):
            bul = True

    return bul


def hay_clases_sin_instalacion(conn):
    print("\n")
    n_id = id_clases_con_instalacion(conn)
    cursor = conn.cursor()
    consulta = "SELECT * FROM CLASE"
    cursor.execute(consulta)
    lista = cursor.fetchall()
    bul = False
    for row in lista:
        cpm = []
        cpm.append(int(row[0]))
        if(not all(item in n_id for item in cpm)):
            bul = True

    return bul


def asignar_entrenador(conn):

    if(hayclases(conn) and hayentrenador(conn) and hay_clases_sin_entrenador(conn)):

        cursor = conn.cursor()
        print("Las clases disponibles son: \n")
        mostrar_clases_sin_entrenador(conn)
        id = int(
            input("Introduzca el ID de la clase a la que quieras añadirle el entrenador: "))
        n_id = id_clases(conn)
        n_id_ent = id_clases_con_entrenador(conn)

        sets = {id}
        if(sets.issubset(n_id) or (not sets.issubset(n_id_ent))):
            print("\nEntrenadores.\n")
            muestraEntrenadores(conn)
            dni = input(
                "Introduzca el DNI del entrenado que desea asignar a esa clase: ")
            while(not existe_entrenador(conn, dni)):
                muestraEntrenadores(conn)
                dni = input("Introduce un DNI correcto: ")

            consulta = "INSERT INTO IMPARTE(DNI,ID_CLASE) values('%s','%s')" % (
                dni, id)
            try:
                cursor.execute(consulta)
                cursor.commit()
            except Exception as ex:
                print(
                    "Los datos introducidos no son correctos o el entrenador está ocupado en ese tramo horario.")
                cursor.rollback()
        else:
            print("\nNinguna clase coincide con el ID introducido.\n")

    else:
        print(
            "No hay clases o entrenadores disponibles o todas las clases tienen entrenador.")


def asignar_instalacion(conn):

    if(hayclases(conn) and hayinstalacion(conn) and hay_clases_sin_instalacion(conn)):

        cursor = conn.cursor()
        print("Las clases disponibles son: \n")
        mostrar_clases_sin_instalacion(conn)

        id = int(
            input("Introduzca el ID de la clase a la que quieras añadirle la instalacion: "))
        n_id = id_clases(conn)
        n_id_ins = id_clases_con_instalacion(conn)

        sets = {id}

        if(sets.issubset(n_id) or (not sets.issubset(n_id_ins))):
            mostrar_instalacion(conn)

            id_i = input(
                "Introduzca el ID de la instalación que va a asignar: ")

            consulta = "INSERT INTO LUGAR(ID_INSTALACION,ID_CLASE) values('%s','%s')" % (
                id_i, id)
            try:
                cursor.execute(consulta)
                cursor.commit()
            except Exception as ex:
                print(
                    "ERROR: La isntalación esta ocupada en ese tramo horario o los datos introducidos no son correctos.")
                cursor.rollback()
        else:
            print("\n Ninguna clase coincide con el ID introducido o esa clase ya tiene una instalación asignada.\n")
    else:
        print("No hay clases o instalaciones disponibles o todas las clases tienen instalacion.")


def gestionClases(conn):
    opcion = 1
    while 1 <= opcion <= 5:
        print("1. Crear una clase.")
        print("2. Borrar clases.")
        print("3. Mostrar clases.")
        print("4. Asignar entrenador a la clase.")
        print("5. Asignar instalación a la clase.")
        print("Cualquier otro número para salir.")

        while True:
            try:
                opcion = int(input("\nElija una opción: \n"))
                break
            except:
                print("Introduce una opción válida")

        os.system('cls' if os.name == 'nt' else 'clear')
        if(opcion == 1):
            crear_clase(conn)
        elif(opcion == 2):
            borrar_clase(conn)
        elif(opcion == 3):
            mostrar_clases(conn)
        elif(opcion == 4):
            asignar_entrenador(conn)
        elif(opcion == 5):
            asignar_instalacion(conn)
