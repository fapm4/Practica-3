import pyodbc

def conectaBase():
    try:
        conn = pyodbc.connect('DRIVER={Devart ODBC Driver for Oracle};Direct=True;Host=oracle0.ugr.es;Service Name=practbd.oracle0.ugr.es;User ID=x8768206;Password=x8768206')
        
    except Exception as ex:
        print(ex)
        
    return conn

def createTables(conn):
    
    try:
        createClase = ''' CREATE TABLE CLASE( 
            id_clase VARCHAR2(9),
            tematica VARCHAR2(40), 
            horario  DATE, 
            CONSTRAINT PK_CLASE PRIMARY KEY(id_clase))'''

        with conn.cursor() as cursor: 
            cursor.execute(createClase)

        createEntrenadores = ''' CREATE TABLE ENTRENADORES(
            DNI VARCHAR2(9),
            NOMBRE VARCHAR2(40),
            APELLIDOS VARCHAR2(40),
            CORREO VARCHAR2(40),
            DIRECCION VARCHAR2(40),
            TELEFONO NUMBER,
            ESPECIALIDAD VARCHAR2(40) CHECK (ESPECIALIDAD='Raqueta' OR ESPECIALIDAD='Equipo' OR ESPECIALIDAD='Personal') ,
            SALARIO NUMBER,
            CONSTRAINT PK_CLIENTES PRIMARY KEY (DNI),
            CONSTRAINT UK_CLIENTES_CORREO UNIQUE (CORREO),
            CONSTRAINT UK_CLIENTES_TELEFONO UNIQUE (TELEFONO))'''

        with conn.cursor() as cursor: 
            cursor.execute(createEntrenadores)

        createClientes = ''' CREATE TABLE CLIENTES(
            DNI VARCHAR2(9),
            NOMBRE VARCHAR2(40),
            APELLIDOS VARCHAR2(40),
            CORREO VARCHAR2(40),
            DIRECCION VARCHAR2(40),
            TELEFONO NUMBER(9),
            TIPO_SUSCRIPCION VARCHAR2(2),
            CONSTRAINT PPK_CLIENTES PRIMARY KEY (DNI),
            CONSTRAINT PUK_CLIENTES_CORREO UNIQUE (CORREO),
            CONSTRAINT PUK_CLIENTES_TELEFONO UNIQUE (TELEFONO))'''

        with conn.cursor() as cursor: 
            cursor.execute(createClientes)

        createInstalacion = ''' CREATE TABLE INSTALACION(
            id_instalacion VARCHAR2(9),
            aforo NUMBER,
            CONSTRAINT IPK_CLASE PRIMARY KEY(id_instalacion))'''

        with conn.cursor() as cursor: 
            cursor.execute(createInstalacion)

        createReserva = ''' CREATE TABLE RESERVA(
            DNI VARCHAR2(9),
            ID_INSTALACION VARCHAR2(9),
            FECHA DATE,
            CONSTRAINT PK_RESERVA PRIMARY KEY(DNI),
            CONSTRAINT FK_RESERVA_INSTALACION FOREIGN KEY(ID_INSTALACION) REFERENCES INSTALACION)'''

        with conn.cursor() as cursor: 
            cursor.execute(createReserva)
        
        createApuntado = ''' CREATE TABLE APUNTADO(
            DNI VARCHAR2(9),
            ID_CLASE VARCHAR2(9),
            CONSTRAINT PK_APUNTADO PRIMARY KEY(DNI),
            CONSTRAINT FK_APUNTADO_CLASE FOREIGN KEY(ID_CLASE) REFERENCES CLASE)'''

        with conn.cursor() as cursor: 
            cursor.execute(createApuntado)

        createImparte = ''' CREATE TABLE IMPARTE(
            DNI VARCHAR2(9),
            id_clase VARCHAR2(9),
            CONSTRAINT EK_CLASEI FOREIGN KEY (id_clase) REFERENCES CLASE,
            CONSTRAINT EK_DNI FOREIGN KEY (DNI) REFERENCES ENTRENADORES,
            CONSTRAINT PK_IMPARTE PRIMARY KEY(id_clase,DNI))'''

        with conn.cursor() as cursor: 
            cursor.execute(createImparte)

        createLugar = ''' CREATE TABLE LUGAR(
            id_instalacion VARCHAR2(9),
            id_clase VARCHAR2(9),
            CONSTRAINT EK_CLASEL FOREIGN KEY (id_clase) REFERENCES CLASE,
            CONSTRAINT EK_INSTALACION FOREIGN KEY (id_instalacion) REFERENCES INSTALACION,
            CONSTRAINT PK_LUGAR PRIMARY KEY(id_clase,id_instalacion))'''

        with conn.cursor() as cursor: 
            cursor.execute(createLugar)

    except Exception as ex:
        print(ex)

def dropBD(conn):
    tablas=["LUGAR", "IMPARTE", "APUNTADO", "RESERVA", "INSTALACION", "CLIENTES", "ENTRENADORES", "CLASE"]
    i=0
    while i < 8:        
        try:
            vaciado = "DROP TABLE " + tablas[i]

            with conn.cursor() as cursor:
                cursor.execute(vaciado)

        except Exception as ex:
            print(ex)
            
            with conn.cursor() as cursor:
                cursor.rollback()
        i+=1
