import sqlite3

class Bbdd:
    def iniciar(self):
        try:
            #Creamos la base de datos, si ya está creada se va a conectar a la misma, no la sobreescribe.
            self.conexion = sqlite3.connect('./torneo_argentino.db')
            #Creamos un cursor para realizar las operaciones dentro de la base de datos
            self.cursor = self.conexion.cursor()
            
        except Exception as e:
            #Si llega a haber algún inconveniente la excepción nos mostrará donde radica para poder intervenir
            print(f'Surgió un error ({e})')

    def crear_tabla(self):
        try:
            #Conecctamos la base de datos
            self.iniciar()
            #Creamos la tabla "temporadad_2022", si por error volvemos a ejecutar esta funcion, no se va a sobrescribir la tabla existente
            self.cursor.execute('''CREATe TABLE IF NOT EXISTS temporada_2022
                          (id INTEGER PRIMARY KEY autoincrement,
                          jornada int not null,
                          equipo_local text not null,
                          goles_local int not null,
                          equipo_visitante text not null,
                          goles_visitante int not null,
                          UNIQUE (jornada,equipo_local,equipo_visitante))''')
            #Commit para confirmar los cambios efectuados
            self.conexion.commit()
            #Cerramos la base de datos
            self.conexion.close()
            
        except Exception as e:
            #Si llega a haber algún inconveniente la excepción nos mostrará donde radica para poder intervenir
            print(f'Surgió un error ({e})')

    # Definimos una funcion para realizar las consultas, con 2 parametros:
    # query: va a ser la consulta
    # fetch: puede fetchall(para todos los valores de la consulta) o fetchone(para el primer valor de la consulta)
    def select(self,query,fetch):
        try:
            #Conecctamos la base de datos
            self.iniciar()
            #Executamos la query ingresada como uno de los pa
            self.cursor.execute(query)
            #Analiza segun el tipo de fetch que elegimos para la consulta
            if fetch == 'fetchall':
                resultado=self.cursor.fetchall()
            else:
                resultado=self.cursor.fetchone()
            #Cerramos la base de datos
            self.conexion.close()
            
            return resultado
        except Exception as e:
            #Si llega a haber algún inconveniente la excepción nos mostrará donde radica para poder intervenir
            print(f'Surgió un error ({e})')

    #Definimos una funcion para realizar el ingreso, modificación o borrado en la tabla, con 2 parametros:
    # query: va a ser la consigna
    # parametros: los valores que llevará la consulta, por defecto es una cadena vacia
    def insert_delete_update(self, query, parametros=''):
        try:
            #Conecctamos la base de datos
            self.iniciar()
            self.cursor.execute(query, parametros)
            #Commit para confirmar los cambios efectuados
            self.conexion.commit()
            #Cerramos la base de datos
            self.conexion.close()
            
        except Exception as e:
            #Si llega a haber algún inconveniente la excepción nos mostrará donde radica para poder intervenir
            return e
            
