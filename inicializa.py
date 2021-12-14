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

        createEntrenadores = ''' CREATE TABLE ENTRENADORES(
            DNI VARCHAR2(9),
            NOMBRE VARCHAR2(20),
            APELLIDOS VARCHAR2(20),
            CORREO VARCHAR2(20),
            DIRECCION VARCHAR2(20),
            TELEFONO NUMBER,
            ESPECIALIDAD VARCHAR2(30) CHECK (ESPECIALIDAD='Raqueta' OR ESPECIALIDAD='Equipo' OR ESPECIALIDAD='Personal') ,
            SALARIO NUMBER DEFAULT 0,
            CONSTRAINT PK_ENTRENADORES PRIMARY KEY (DNI),
            CONSTRAINT UK_ENTRENADORES_CORREO UNIQUE (CORREO),
            CONSTRAINT UK_ENTRENADORES_TELEFONO UNIQUE (TELEFONO))
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createEntrenadores)

        createClientes = ''' CREATE TABLE CLIENTES(
            DNI VARCHAR2(9),
            NOMBRE VARCHAR2(20),
            APELLIDOS VARCHAR2(20),
            CORREO VARCHAR2(20),
            DIRECCION VARCHAR2(20),
            TELEFONO NUMBER,
            TIPO_SUSCRIPCION VARCHAR2(2),
            CONSTRAINT PK_CLIENTES PRIMARY KEY (DNI),
            CONSTRAINT UK_CLIENTES_CORREO UNIQUE (CORREO),
            CONSTRAINT UK_CLIENTES_TELEFONO UNIQUE (TELEFONO))
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createClientes)

        createInstalacion = ''' CREATE TABLE INSTALACION(
            id_instalacion VARCHAR2(9),
            aforo NUMBER,
            CONSTRAINT IPK_CLASE PRIMARY KEY(id_instalacion))
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createInstalacion)

        createReserva = ''' CREATE TABLE RESERVA(
            DNI VARCHAR2(9),
            ID_INSTALACION VARCHAR2(9),
            FECHA DATE,
            CONSTRAINT PK_RESERVA PRIMARY KEY(DNI),
            CONSTRAINT FK_RESERVA_INSTALACION FOREIGN KEY(ID_INSTALACION) REFERENCES INSTALACION)
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createReserva)
        
        createApuntado = ''' CREATE TABLE APUNTADO(
            DNI VARCHAR2(9),
            ID_CLASE VARCHAR2(9),
            CONSTRAINT PK_APUNTADO PRIMARY KEY(DNI),
            CONSTRAINT FK_APUNTADO_CLASE FOREIGN KEY(ID_CLASE) REFERENCES CLASE)
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createApuntado)

        createImparte = ''' CREATE TABLE IMPARTE(
            DNI VARCHAR2(9),
            id_clase VARCHAR2(9),
            CONSTRAINT EK_CLASEI FOREIGN KEY (DNI) REFERENCES ENTRENADORES (DNI)  ON DELETE CASCADE,
            CONSTRAINT EK_DNI FOREIGN KEY (id_clase) REFERENCES CLASE (id_clase)  ON DELETE CASCADE,
            CONSTRAINT PK_IMPARTE PRIMARY KEY(id_clase,DNI)
            )
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createImparte)

        createLugar = ''' CREATE TABLE LUGAR(
            id_instalacion VARCHAR2(9),
            id_clase VARCHAR2(9),
            CONSTRAINT EK_CLASEL FOREIGN KEY (id_clase) REFERENCES CLASE (id_clase) ON DELETE CASCADE,
            CONSTRAINT EK_INSTALACION FOREIGN KEY (id_instalacion) REFERENCES INSTALACION (id_instalacion) ON DELETE CASCADE,
            CONSTRAINT PK_LUGAR PRIMARY KEY(id_clase,id_instalacion)
            )
        '''

        with conn.cursor() as cursor: 
            cursor.execute(createLugar)

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
        triggerEntrenador = """
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
            cursor.commit()
                
        with conn.cursor() as cursor: 
            cursor.execute(triggerEntrenador)

    except Exception as ex:
        print(ex)

def dropBD(conn):
    tablas=["LUGAR", "IMPARTE", "APUNTADO", "RESERVA", "INSTALACION", "CLIENTES", "ENTRENADORES", "CLASE"]
    i=0
    while i < len(tablas):        
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
