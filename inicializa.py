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
            APELLIDOS VARCHAR2(40),
            CORREO VARCHAR2(60),
            DIRECCION VARCHAR2(60),
            TELEFONO NUMBER(9),
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
            CLASES_APUNTADAS NUMBER(1),
            CONSTRAINT CK_MAX_CLASES CHECK (CLASES_APUNTADAS >=0 AND CLASES_APUNTADAS <= 25),
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
            CONSTRAINT FK_RESERVA_INSTALACION_RESERVA FOREIGN KEY(ID_INSTALACION) REFERENCES INSTALACION ON DELETE CASCADE)
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createReserva)
            cursor.commit()
        
        createApuntado = ''' CREATE TABLE APUNTADO(
            DNI VARCHAR2(9),
            ID_CLASE VARCHAR2(9),
            CONSTRAINT FK_APUNTADO FOREIGN KEY (DNI) REFERENCES CLIENTES (DNI) ON DELETE CASCADE,
            CONSTRAINT FK_APUNTADO_CLASE FOREIGN KEY (ID_CLASE) REFERENCES CLASE (ID_CLASE) ON DELETE CASCADE,
            CONSTRAINT PK_APUNTADO PRIMARY KEY(DNI,ID_CLASE)
            )
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
            CONSTRAINT EK_CLASEL FOREIGN KEY (id_clase) REFERENCES CLASE (id_clase) ON DELETE CASCADE,
            CONSTRAINT EK_INSTALACION FOREIGN KEY (id_instalacion) REFERENCES INSTALACION (id_instalacion) ON DELETE CASCADE,
            CONSTRAINT PK_LUGAR PRIMARY KEY(id_clase,id_instalacion))
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createLugar)
            cursor.commit()

        createReservaHistorico = ''' CREATE TABLE RESERVA_HISTORICO(
            DNI VARCHAR2(9),
            ID_INSTALACION VARCHAR2(9),
            FECHA DATE,
            CONSTRAINT PK_RESERVA_HIST PRIMARY KEY(DNI),
            CONSTRAINT FK_RESERVA_INSTALACION FOREIGN KEY(ID_INSTALACION) REFERENCES INSTALACION ON DELETE CASCADE) 
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createReservaHistorico)
            cursor.commit()

        # Triggers

        triggerInstalacion =  """
            create or replace trigger NO_OCUPADA
            before insert 
            ON LUGAR
            FOR EACH ROW

            DECLARE 
                v_horario_instalacion  clase.horario%TYPE;
                fechaAux clase.horario%TYPE;

                    
            BEGIN
                select horario INTO fechaAux from clase where id_clase=:new.id_clase;

                FOR I IN(SELECT * FROM LUGAR WHERE id_instalacion=:new.id_instalacion)
                    LOOP
                    SELECT HORARIO into v_horario_instalacion FROM CLASE WHERE id_clase=I.id_clase;
                    IF (v_horario_instalacion=fechaAux) then
                            raise_application_error(-20600,:new.id_instalacion ||' La instalación está ocupada a la en el horario de esa clase.'); 
                    END IF;
                    END LOOP;
            END;
        """

        with conn.cursor() as cursor: 
            cursor.execute(triggerInstalacion)        


        triggerEntrenador =  """
            create or replace trigger NO_OCUPADO
            before insert 
            ON IMPARTE
            FOR EACH ROW

            DECLARE 
                v_horario_entrenador  clase.horario%TYPE;
                fechaAux clase.horario%TYPE;

                    
            BEGIN
                select horario INTO fechaAux from clase where id_clase=:new.id_clase;

                FOR I IN(SELECT * FROM IMPARTE WHERE dni=:new.dni)
                    LOOP
                    SELECT HORARIO into v_horario_entrenador FROM CLASE WHERE id_clase=I.id_clase;
                    IF (v_horario_entrenador=fechaAux) then
                            raise_application_error(-20600,:new.dni ||' El entrenador está ocupado en el horario de esa clase.'); 
                    END IF;
                    END LOOP;
            END;
        """

        with conn.cursor() as cursor: 
            cursor.execute(triggerEntrenador)  
            
        triggerCaracterTelefono = '''
        CREATE OR REPLACE TRIGGER CONTROL_TELEFONO
        BEFORE INSERT OR UPDATE ON CLIENTES FOR EACH ROW
        WHEN (NEW.TELEFONO = -1)
        BEGIN
            raise_application_error(-20601,'Ha introducido un carácter alfabético en el campo teléfono');
        END;'''

        with conn.cursor() as cursor: 
            cursor.execute(triggerCaracterTelefono)
            cursor.commit()

        triggerControlCorreo = '''
        CREATE OR REPLACE TRIGGER CONTROL_CORREO
        BEFORE INSERT OR UPDATE ON CLIENTES FOR EACH ROW
        WHEN (NEW.CORREO NOT LIKE '_%@__%.__%')
        BEGIN
            raise_application_error(-20600,'Ha introducido un carácter alfabético en el campo teléfono');
        END;'''

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
        END;'''

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
                    IF LETRA NOT IN ('A' ,'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z') THEN
                        raise_application_error(-20603,'Formato de DNI incorrecto');
                    END IF;
                END IF; 
            END;'''

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
        END;'''

        with conn.cursor() as cursor: 
            cursor.execute(triggerControlLongitudTelefono)
            cursor.commit()

        triggerControlClasesApuntadas = '''
        CREATE OR REPLACE TRIGGER CONTROL_CLASES_APUNTADAS
        AFTER UPDATE OF CLASES_APUNTADAS
        ON CLIENTES FOR EACH ROW
        BEGIN
            IF(:NEW.TIPO_SUSCRIPCION = 'NORMAL') THEN
                IF(:NEW.CLASES_APUNTADAS >= 6) THEN
                    raise_application_error(-20605, 'Número de máximo de clases alcanzada');
                END IF;
            ELSIF (:NEW.TIPO_SUSCRIPCION = 'MEDIO') THEN
                IF (:NEW.CLASES_APUNTADAS >= 16) THEN 
                    raise_application_error(-20606, 'Número de máximo de clases alcanzada');
                END IF;
            ELSIF (:NEW.TIPO_SUSCRIPCION = 'PREMIUM') THEN
                IF (:NEW.CLASES_APUNTADAS >= 26) THEN
                    raise_application_error(-20607, 'Número de máximo de clases alcanzada');
                END IF;
            END IF;
        END;'''

        with conn.cursor() as cursor: 
            cursor.execute(triggerControlClasesApuntadas)
            cursor.commit()

        trigger_entrenadores='''
            CREATE OR REPLACE TRIGGER existe
            BEFORE INSERT ON ENTRENADORES
            FOR EACH ROW 
            DECLARE
                cuantos NUMBER(1):=0;
                aux_dni ENTRENADORES.DNI%TYPE;
            BEGIN
                SELECT COUNT(*) INTO cuantos FROM ENTRENADORES
                WHERE DNI = :new.DNI;
                IF (cuantos>0) THEN
                    SELECT DNI INTO aux_dni FROM ENTRENADORES WHERE DNI=:NEW.DNI;
                    RAISE_APPLICATION_ERROR(-20601,aux_dni||' ese DNI ya existe en la base de datos');
                END IF;
            END;
        '''

        with conn.cursor() as cursor: 
            cursor.execute(trigger_entrenadores)
            cursor.commit()
            
        triggerDNIcorrecto = '''
            CREATE OR REPLACE TRIGGER formatoDNI
            BEFORE INSERT OR UPDATE OF DNI ON ENTRENADORES 
            FOR EACH ROW
            DECLARE
                LETRA VARCHAR2(1);
            BEGIN
                SELECT SUBSTR(:new.DNI,9,9) INTO LETRA FROM DUAL;
                IF (:new.DNI NOT LIKE '_________') THEN
                    raise_application_error(-20603,'El DNI ha de tener 9 caracteres');
                ELSE 
                    IF LETRA NOT IN ('A' ,'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z') THEN
                        raise_application_error(-20603,'El ultimo caracter del DNI ha de ser una letra');
                    END IF;
                END IF; 
            END;'''

        with conn.cursor() as cursor: 
            cursor.execute(triggerDNIcorrecto)
            cursor.commit()

        triggerLargoTlfe = '''
            CREATE OR REPLACE TRIGGER largotlf
            BEFORE INSERT ON ENTRENADORES 
            FOR EACH ROW
            WHEN (new.telefono NOT LIKE '_________')
            BEGIN
                raise_application_error(-20601,'El telefono ha de tener 9 digitos');
            END;
        '''

        with conn.cursor() as cursor: 
            cursor.execute(triggerLargoTlfe)
            cursor.commit()

        #triggerReservaHistorico = """CREATE TRIGGER trigger_reserva_historico
        #AFTER INSERT ON reserva
        #FOR EACH ROW
        #BEGIN
        #INSERT INTO reserva_historico(dni,id_instalacion,fecha)
        #VALUES (NEW.dni, NEW.id_instalacion, NEW.fecha);
        #END;

        #with conn.cursor() as cursor: 
        #    cursor.execute(triggerReservaHistorico)
        #    cursor.commit()

    except Exception as ex:
        print(ex)

#In [ ]:

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

