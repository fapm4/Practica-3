from datetime import date
import pyodbc


def max_id(conn):
    cursor = conn.cursor()
    cursor.execute("select id_clase from CLASE")
    lit = cursor.fetchall()
    if( len(lit) <= 0):
        id = -1
    else:
        id = int(lit[len(lit)-1][0])

    cursor.commit()
    
    return id

def crear_clase(conn):
    cursor = conn.cursor()
    tematica = input("Introduce la temática de la clase: ")
    dia =(input("Introduce el día en el que tentrá lugar la clase: "))
    hora = (input("Introduce la hora a la que tendrá lugar la clase: "))
    atributos  =[tematica,dia,hora]
    fecha = date.today()
    id = max_id(conn)
    id+=1

    f = "TO_DATE('" + str(fecha.year) + "/" + str(fecha.month) + "/"+ atributos[1] + " " + atributos[2] +":00:00','YYYY/MM/DD HH24:MI:SS')"
    """
    v= "values ('" + str(id) +"','" + atributos[0] + "'," + f +"));"
    consulta = "INSERT INTO CLASE (id_clase,tematica,horario) " + v
    """
    consulta = "INSERT INTO CLASE (id_clase,tematica,horario)  values ('%s','%s',%s)"%(id,atributos[0],f)
    print(consulta)
    try:
        cursor.execute(consulta)
        cursor.commit()
    except Exception as ex:
        print(ex)
        cursor.rollback()

    return atributos


def borrar_clase(conn):
    mid = max_id(conn)
    print(mid)
    cursor = conn.cursor()

    if(mid != -1):
        try:
            i = int(input("Introduzca el id de la clase que quiera borrar.\n-1 para borrar todas la clases: "))
            if(i == -1):
                consulta ="DELETE FROM CLASE"
                try:
                    cursor.execute(consulta)
                    cursor.commit()
                    
                except Exception as ex:
                    print(ex)
                    cursor.rollback()
            elif(-1 <= i <=mid):
                consulta = "DELETE FROM CLASE WHERE id_clase='%s'"%(i)
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
            msg = ("ID: %s Temática: %s  Fecha: %s")%(row[0],row[1],row[2])
            print(msg)
            print("\n")
    cursor.commit()


    
    
def gestionClases(conn):
    id = -1
    while True:
        id+=1
        print("1. Crear una clase.")
        print("2. Borrar clases.")
        print("3. Mostrar clases.")
        opcion =int(input("\nElija una opción: "))

        if(opcion == 1):
            crear_clase(conn)
        elif(opcion ==2):
            borrar_clase(conn)
        elif(opcion==3):
            mostrar_clases(conn)