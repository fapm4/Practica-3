#!/usr/bin/env python
# coding: utf-8

# Practica 3

# In[ ]:

import pyodbc
import inicializa
import subsistema_clientes
import subsistema_entrenadores
import subsistema_clases
import subsistema_instalacion

import os

from time import gmtime, strftime

def conectaBase():
    conn = type(pyodbc.connect)
    try:
        conn = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0.ugr.es;Service Name=practbd.oracle0.ugr.es;User ID=x8768206;Password=x8768206')
        conn.autocommit = False
        
    except Exception as ex:
        print(ex)
        
    return conn

def main():
    conn = conectaBase()

    print("Bienvenido al Centro Deportivo Epicardo.\nIndica a continuación una de las opciones.")
    print('\n')
    
    val = 1

    while val != 5:
        print('0. Inicializar la base de datos')
        print('1. Gestión de Clientes')
        print('2. Gestión de Entrenadores')
        print('3. Gestión de Clases')
        print('4. Gestión de Instalaciones')
        print('5. Salir')
        print('Introduce opción: ')
        val = int(input())
        
        os.system('cls' if os.name == 'nt' else 'clear')
        if val != 5:
            if val == 0:
                inicializa.dropBD(conn)
                inicializa.createTables(conn)
            elif val == 1:
                subsistema_clientes.gestionClientes(conn)
            elif val == 2:
                subsistema_entrenadores.gestionEntrenadores(conn)
            elif val == 3:
                subsistema_clases.gestionClases(conn)
            elif val == 4:
                subsistema_instalacion.gestionInstalacion(conn)
        else:
            with conn.cursor() as cursor:
                cursor.rollback()

    conn.close()

main()
