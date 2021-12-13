#!/usr/bin/env python
# coding: utf-8

import pyodbc
import subsistema_clases
from time import gmtime, strftime
from datetime import date

def conectaBase():

    try:
        conn = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0.ugr.es;Service Name=practbd.oracle0.ugr.es;User ID=x7021155;Password=x7021155')
        conn.autocommit = False
        cursor = conn.cursor()
    except Exception as ex:
        print(ex)
        
    return conn


def main():

    print("Practica 3")
    print('\n')
    conn = conectaBase()
    cursor = conn.cursor()
    id = -1
    while True:
        id+=1
        print("1. Crear una clase.")
        print("2. Borrar tablas.")
        print("3. Crear tablas.")
        print("4. Borrar clases.")
        opcion =int(input("\nElija una opción: "))

        if(opcion == 1):
            atributos = subsistema_clases.crear_clase()
            fecha = date.today()
            
            f = "TO_DATE('" + str(fecha.year) + "/" + str(fecha.month) + "/"+ atributos[1] + " " + atributos[2] +":00:00','YYYY/MM/DD HH:MI:SS')"
            """
            v= "values ('" + str(id) +"','" + atributos[0] + "'," + f +"));"
            consulta = "INSERT INTO CLASE (id_clase,tematica,horario) " + v
            """
            consulta = "INSERT INTO CLASE (id_clase,tematica,horario)  values ('%s','%s',%s)"%(id,atributos[0],f)
            try:
                cursor.execute(consulta)
                cursor.commit()
            except Exception as ex:
                print(ex)
                cursor.rollback
            
            print(consulta)
        
        if(opcion ==2):
            subsistema_clases.dropBD(conn)
        if(opcion ==3):
            subsistema_clases.createTables(conn)
        if(opcion ==4):
            subsistema_clases.BorrarClases(conn)

             
             



main()