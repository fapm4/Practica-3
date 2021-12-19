
#!/usr/bin/env python
# coding: utf-8

# Practica 3

# In[ ]:

import pyodbc

def createTables(conn):

    try:
        createClase = ''' CREATE TABLE CLASE( 
            id_clase VARCHAR2(9),
            tematica VARCHAR2(20), 
            horario  DATE, 
            CONSTRAINT PK_CLASE PRIMARY KEY(id_clase))
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createClase)
            cursor.commit()

        createEntrenadores = ''' CREATE TABLE ENTRENADORES(
            DNI VARCHAR2(9),
            NOMBRE VARCHAR2(20),
            APELLIDOS VARCHAR2(20),
            CORREO VARCHAR2(60),
            DIRECCION VARCHAR2(60),
            TELEFONO NUMBER,
            ESPECIALIDAD VARCHAR2(30) CHECK (ESPECIALIDAD='Raqueta' OR ESPECIALIDAD='Equipo' OR ESPECIALIDAD='Personal') ,
            SALARIO NUMBER DEFAULT 0,
            CONSTRAINT PK_ENTRENADORES PRIMARY KEY (DNI),
            CONSTRAINT UK_ENTRENADORES_CORREO UNIQUE (CORREO),
            CONSTRAINT UK_ENTRENADORES_TELEFONO UNIQUE (TELEFONO))
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createEntrenadores)
            cursor.commit()

        createClientes = '''CREATE TABLE CLIENTES(
            DNI VARCHAR2(9),
            NOMBRE VARCHAR2(40),
            APELLIDOS VARCHAR2(40),
            CORREO VARCHAR2(60),
            DIRECCION VARCHAR2(40),
            TELEFONO NUMBER(9),
            TIPO_SUSCRIPCION VARCHAR2(9),
            CONSTRAINT PK_CLIENTES PRIMARY KEY (DNI),
            CONSTRAINT UK_CLIENTES_CORREO UNIQUE (CORREO),
            CONSTRAINT UK_CLIENTES_TELEFONO UNIQUE (TELEFONO),
            CONSTRAINT CK_CLIENTES CHECK (TIPO_SUSCRIPCION IN ('NORMAL', 'MEDIO', 'PREMIUM')))'''

        with conn.cursor() as cursor: 
            cursor.execute(createClientes)
            cursor.commit()

        createInstalacion = ''' CREATE TABLE INSTALACION(
            id_instalacion VARCHAR2(9),
            aforo NUMBER,

            CONSTRAINT IPK_CLASE PRIMARY KEY(id_instalacion))
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createInstalacion)
            cursor.commit()

        createReserva = ''' CREATE TABLE RESERVA(
            DNI VARCHAR2(9),
            ID_INSTALACION VARCHAR2(9),
            FECHA DATE,
            CONSTRAINT PK_RESERVA PRIMARY KEY(DNI),
            CONSTRAINT FK_RESERVA_INSTALACION FOREIGN KEY(ID_INSTALACION) REFERENCES INSTALACION)
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createReserva)
            cursor.commit()
        
        createApuntado = ''' CREATE TABLE APUNTADO(
            DNI VARCHAR2(9),
            ID_CLASE VARCHAR2(9),
            CONSTRAINT PK_APUNTADO PRIMARY KEY(DNI),
            CONSTRAINT FK_APUNTADO_CLASE FOREIGN KEY(ID_CLASE) REFERENCES CLASE)
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createApuntado)
            cursor.commit()

        createImparte = ''' CREATE TABLE IMPARTE(
            DNI VARCHAR2(9),
            id_clase VARCHAR2(9),
            CONSTRAINT EK_CLASEI FOREIGN KEY (id_clase) REFERENCES CLASE (id_clase) ON DELETE CASCADE,
            CONSTRAINT EK_DNI FOREIGN KEY (DNI) REFERENCES ENTRENADORES (DNI) ON DELETE CASCADE,
            CONSTRAINT PK_IMPARTE PRIMARY KEY(id_clase,DNI))
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createImparte)
            cursor.commit()

        createLugar = ''' CREATE TABLE LUGAR(
            id_instalacion VARCHAR2(9),
            id_clase VARCHAR2(9),
            CONSTRAINT EK_CLASEL FOREIGN KEY (id_clase) REFERENCES CLASE,
            CONSTRAINT EK_INSTALACION FOREIGN KEY (id_instalacion) REFERENCES INSTALACION,
            CONSTRAINT PK_LUGAR PRIMARY KEY(id_clase,id_instalacion))
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createLugar)
            cursor.commit()

        triggerCaracterTelefono = '''
        CREATE OR REPLACE TRIGGER CONTROL_TELEFONO
        BEFORE INSERT OR UPDATE ON CLIENTES FOR EACH ROW
        WHEN (NEW.TELEFONO = -1)
        BEGIN
            raise_application_error(-20601,'Ha introducido un carácter alfabético en el campo teléfono');
        END;
        '''

        with conn.cursor() as cursor: 
            cursor.execute(triggerCaracterTelefono)
            cursor.commit()

        triggerControlCorreo = '''
        CREATE OR REPLACE TRIGGER CONTROL_CORREO
        BEFORE INSERT OR UPDATE ON CLIENTES FOR EACH ROW
        WHEN (NEW.CORREO NOT LIKE '_%@__%.__%')
        BEGIN
            raise_application_error(-20600,'Ha introducido un carácter alfabético en el campo teléfono');
        END;
        '''

        with conn.cursor() as cursor: 
            cursor.execute(triggerControlCorreo)
            cursor.commit()


        triggerControlSuscripcion = '''
        CREATE OR REPLACE TRIGGER CONTROL_SUSCRIPCION
        BEFORE UPDATE OF TIPO_SUSCRIPCION 
        ON CLIENTES FOR EACH ROW
        WHEN (NEW.TIPO_SUSCRIPCION NOT IN ('NORMAL', 'MEDIO', 'PREMIUM'))
        BEGIN
            raise_application_error(-20602,'Se ha introducido un tipo de suscripción no válido');
        END;
        '''

        with conn.cursor() as cursor: 
            cursor.execute(triggerControlSuscripcion)
            cursor.commit()

        triggerControlFormatoDNI = '''
            CREATE OR REPLACE TRIGGER CONTROL_DNI
            BEFORE INSERT OR UPDATE OF DNI 
            ON CLIENTES FOR EACH ROW
            DECLARE
                LETRA VARCHAR2(1);
            BEGIN
                SELECT SUBSTR(:NEW.DNI,9,9) INTO LETRA FROM DUAL;
                IF (:NEW.DNI NOT LIKE '_________') THEN
                    raise_application_error(-20603,'Formato de DNI incorrecto');
                ELSE 
                    IF LETRA NOT IN ('A' ,'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z') THEN
                        raise_application_error(-20603,'Formato de DNI incorrecto');
                    END IF;
                END IF; 
        END;
        '''

        with conn.cursor() as cursor: 
            cursor.execute(triggerControlFormatoDNI)
            cursor.commit()

        triggerControlLongitudTelefono = '''
        CREATE OR REPLACE TRIGGER CONTROL_LONGITUD_TELEFONO
        BEFORE INSERT OR UPDATE ON CLIENTES 
        FOR EACH ROW
        WHEN (NEW.TELEFONO NOT LIKE '_________')
        BEGIN
            raise_application_error(-20604,'Longitud de teléfono no válida');
        END;
        '''

        with conn.cursor() as cursor: 
            cursor.execute(triggerControlLongitudTelefono)
            cursor.commit()
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
                cursor.commit()

        except Exception as ex:
            print(ex)
            
            with conn.cursor() as cursor:
                cursor.rollback()
        i+=1
