#!/usr/bin/env python
# coding: utf-8

# Practica 3

# In[ ]:

import pyodbc
import inicializa
import subsistema_entrenadores
import subsistema_clases

import os

from time import gmtime, strftime

def conectaBase():
    try:
        conn = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0.ugr.es;Service Name=practbd.oracle0.ugr.es;User ID=x7390452;Password=x7390452')
        conn.autocommit = False
        cursor = conn.cursor()
        
    except Exception as ex:
        print(ex)
        
    return conn

def main():
    conn = conectaBase()

    print("Bienvenido al Centro Deportivo Epicardo.\nIndica a continuación una de las opciones.")
    print('\n')
    
    val = 1

    while val != 5:
        print('0. Inicializar la base de datos\n')
        print('1. Gestión de Clientes\n')
        print('2. Gestión de Entrenadores\n')
        print('3. Gestión de Clases\n')
        print('4. Gestión de Instalaciones\n')
        print('5. Salir\n')
        print('Introduce opción: ')
        val = int(input())
        
        os.system('cls' if os.name == 'nt' else 'clear')
        if val != 5:
            if val == 0:
                inicializa.dropBD(conn)
                inicializa.createTables(conn)
            elif val == 1:
                print('Esta parte es de Pancho\n')
            elif val == 2:
                subsistema_entrenadores.gestionEntrenadores(conn)
            elif val == 3:
                subsistema_clases.gestionClases(conn)
            elif val == 4:
                print('Esta parte es de Fjorn\n')
        else:
            with conn.cursor() as cursor:
                cursor.rollback()

    conn.close()

main()