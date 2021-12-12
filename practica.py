import pyodbc
from time import gmtime, strftime

def conectaBase():
    
    try:
        # Server dependerá de cada nombre del server en SQL Server cuando sea EXPRESS
        # Database obviamente también
        conn = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0.ugr.es;Service Name=practbd.oracle0.ugr.es;User ID=x8768206;Password=x8768206')
        
    except Exception as ex:
        print(ex)
        
    return conn

def creaTablas(conn):
    createClase = "CREATE TABLE CLASE( id_clase VARCHAR2(9), tematica VARCHAR2(20), horario  DATE, CONSTRAINT PK_CLASE PRIMARY KEY(id_clase))"
    print("Hola")
    with conn.cursor() as cursor: 
        print("Hola")
        cursor.execute(createClase)

def main():
    con = conectaBase()
    creaTablas(con)

main()