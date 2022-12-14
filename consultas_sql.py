import sqlite3
from script_sql import Bbdd
import pandas as pd


class ConsultasSQL(Bbdd):
    def __init__(self):
        self.iniciar()
        self.tabla_equipos()

    # Creamos una tabla con los equipos, para utilizarlo en futuros filtros de las las tablas
    def tabla_equipos(self):
        query_equipos = '''CREATE TABLE IF NOT EXISTS equipos_2022 as
						SELECT DISTINCT(equipo_local)as equipo 
						FROM temporada_2022 
						ORDER BY equipo'''
        self.cursor.execute(query_equipos)
        self.conexion.commit()
        self.conexion.close()

    # Script para la tabla de posiciones completa, con el campo de "ORDER BY" con la posibilidad de modificarlo para diferentes consultas. Por defecto la tabla está ordenada por los puntos totales en orden descendiente
    def query_tabla_posiciones(self, order_by='Puntos desc'):
        # Se realiza la union de 2 tablas la de visitante y local sumando los totales de cada columna
        # NOMENCLATURA: PJ:partidos jugados, PG:partidos ganados, PE:partidos empatados, PP:partidos perdidos,
        #	GF:goles a favor, GC:goles en contra, GT: diferencia de goles entre a favor y en contra,
        #	Puntos:Total de puntos obtenidos (3 puntos por cada PG, 1 punto por cada PE)
        query = f'''SELECT equipo as Equipo, sum(PJ) as PJ, sum(PG) PG, sum(PE) PE, sum(PP) PP, sum(GF) GF, sum(GC) GC , sum(GF)-sum(GC) as GT,
					sum(PG*3 + PE) as Puntos
				from (
					SELECT equipo,  
						sum( case when "equipo_local" = "equipo" THEN 1 
						else 0 end) as PJ,
						sum(case when "goles_local" > "goles_visitante" THEN 1 
						else 0 end) as PG,
						sum(case when "goles_local" = "goles_visitante" THEN 1 
						else 0 end) as PE,
						sum(case when "goles_local" < "goles_visitante" THEN 1 
						else 0 end) as PP,
						sum(goles_local) as GF,
						sum(goles_visitante) as GC
					FROM equipos_2022 
					INNER JOIN temporada_2022 
						on equipo = equipo_local
					GROUP by equipo
					UNION
					SELECT equipo,
						sum( case when "equipo_visitante" = "equipo" THEN 1 
						else 0 end) as PJ,
						sum(case when "goles_local" < "goles_visitante" THEN 1 
						else 0 end) as PG,
						sum(case when "goles_local" = "goles_visitante" THEN 1 
						else 0 end) as PE,
						sum(case when "goles_local" > "goles_visitante" THEN 1 
						else 0 end) as PP,
						sum(goles_visitante) as GF,
						sum(goles_local) as GC
					FROM equipos_2022
					INNER JOIN temporada_2022 
						on equipo = equipo_visitante
					GROUP by equipo)
				group by equipo
				ORDER by {order_by}'''
        return query

    # Como parametros indicamos si se visualiza los datos en la terminal o no. Por defecto no se muestra
    def query_resultados(self, terminal=False):
        # Se realiza el conteo de partidos ganados de local, visitante y empates.
        query = '''SELECT 
		sum(CASE  WHEN "goles_local" > "goles_visitante" THEN 1 ELSE 0 END) as "Victorias Locales",
		sum(CASE  WHEN "goles_local" < "goles_visitante" THEN 1 ELSE 0 END) as "Victorias Visitante",
		sum(CASE  WHEN "goles_local" = "goles_visitante" THEN 1 ELSE 0 END) as "Empates"
		FROM temporada_2022'''
        resultados = self.select(query, 'fetchone')
        conexion = sqlite3.connect('torneo_argentino.db')
        df = pd.read_sql_query(query, conexion)

         # Damos a elegir si se quiere mostrar por terminal
        if terminal:
            print('')
            index = 0
            for i in df:
                if index == 0:
                    print(f'\t - {self.color_nombre(i)} = {self.descripcion_color(resultados[index])}')
                    index += 1
                else:
                    print(f'\t - {self.color_nombre(i)} = {self.descripcion_color(resultados[index])}')
                    index += 1
            print('')

            # Se imprime los datos de la tabla con Pandas
            #print('\n', df, '\n')

        # Devolvemos los resultados para generar graficos de ser necesario
        return df

    # Promedio de resultados
    # Definimos la fucion con el parametro "terminal" para que nos muestre en terminal o no. Por defecto no se muestra
    def query_promedio_resultados(self, terminal=False):
        # Se realiza el conteo de partidos ganados de local, visitante y empates y se los divide por el total de partidos
        # Para que nos de como resultado números decimales en lugar de dividir por 100, realizamos la multiplicación por 0.01 y todo eso lo redondeamos a 2 valores decimales
        query = '''SELECT count(jornada) as "Cantidad de partidos",
		round(sum(CASE  WHEN "goles_local" > "goles_visitante" THEN 1 ELSE 0 END) / (count(jornada)*0.01),2) as "Porcentaje Victorias Locales",
		round(sum(CASE  WHEN "goles_local" < "goles_visitante" THEN 1 ELSE 0 END) / (count(jornada)*0.01),2) as "Porcentaje Victorias Visitante",
		round(sum(CASE  WHEN "goles_local" = "goles_visitante" THEN 1 ELSE 0 END)/ (count(jornada)*0.01),2) as "Porcentaje Empates"
		FROM temporada_2022'''
        resultados = self.select(
            query, 'fetchone')  # fetchone porque solo vamos a tener una lista de elementos

        # Para aplicar Pandas se utiliza la funcion read_sql_query, y para ello necesitamos el parametro con los datos de conexión por ello es que lo formulamos en la variable conexion.
        conexion = sqlite3.connect('torneo_argentino.db')
        df = pd.read_sql_query(query, conexion)

         # Damos a elegir si se quiere mostrar por terminal
        if terminal:
            print('')
            index = 0
            for i in df:
                if index == 0:
                    print(f'\t - {self.color_nombre(i)} = {self.descripcion_color(resultados[index])}')
                    index += 1
                else:
                    print(f'\t - {self.color_nombre(i)} = {self.descripcion_color(resultados[index])} %')
                    index += 1
            print('')

            #print('\n', df, '\n')

        # Devolvemos los resultados para generar graficos de ser necesario
        return df

    # Equipo goleador de la fecha
    # La función tiene como parametro "mostrar_jornada" para que se elija de que jornada visualizar los datos
    # Por defecto esta vacio que devuelve cada uan de las jornadas
    def query_mas_goles_jornada(self, mostrar_jornada=''):
        # Lista donde ingresaremos cada una de las diferentes jornadas realizadas
        lista_jornada = []
        query_jornada = '''Select distinct jornada from temporada_2022 order by id'''
        self.iniciar()
        lista_jornada.append(self.select(query_jornada, 'fetchall'))

        # En este diccionario pondremos de cada una de las jornadas los goles maximos y cuales son los equipos que los realizaron
        jornada_goleador = {}

        # Query para obtener el valor de gol maximo de cada jornada
        jornada_max_gol = '''SELECT jornada, max(max(goles_local), max(goles_visitante)) as 'Máximo anotador de la jornada'
		FROM temporada_2022
		where jornada like ?
		GROUP by jornada
		ORDER by id'''

        # Query para buscar las coincidencias de cada partido segun el maximo de goles.Si no hay coicidencia devuelve NULL y despues lo eliminamos.
        query_equipo_goleador = '''SELECT * from (
		SELECT CASE when goles_local = ?  AND goles_visitante = ? then equipo_local END local,
			CASE when goles_local = ? aND goles_visitante = ? then equipo_visitante END visitante,
			case when goles_local = ? AND goles_visitante = ? then NULL 
				WHEN goles_local = ? THEN equipo_local 
				WHEN goles_visitante = ? THEN equipo_visitante 
				end indistinto
		FROM temporada_2022
		WHERE jornada like  ? 
		order by id) as  equipo_goleador
		where local is not null or  visitante is not null or indistinto is not null
		'''

        # Recorremos el total de jornadas para crear nuestro diccionario
        for i in range(len(lista_jornada[0])):

            for jornada in lista_jornada:
                # Creamos un diccionario para los goles
                dict_goles = {}
                # Creamos un diccionario para los equipos
                dict_equipos_goleadores = {}
                # Como puede haber mas de un equipo ganador los pondremos en una lista
                equipo_goleador = []

                self.iniciar()
                self.cursor.execute(jornada_max_gol, (jornada[i]))
                # en la variable almacenamos el máximo de goles de la jornada
                gol = self.cursor.fetchone()

                # Buscamos los equipos que en la jornada cumplan con el requisito
                self.cursor.execute(query_equipo_goleador, (
                    gol[1], gol[1], gol[1], gol[1], gol[1], gol[1], gol[1], gol[1], jornada[i][0]))
                equipos = self.cursor.fetchall()

                # En este "for" limpiamos los valores null que nos devuelve en cada no coincidencia.
                for partido in range(len(equipos)):
                    for equipo in equipos[partido]:
                        if equipo != None:
                            # Los almacenamos en la lista que creamos anteriormente
                            equipo_goleador.append(equipo)

                # Agregamos los goles del diccionario
                dict_goles['Cantidad_de_goles'] = gol[1]
                # Agregamos los equipos al diccionario
                dict_equipos_goleadores['equipos'] = equipo_goleador
                # Agreamos la jordada y en su interior sus respectivos datos de goles y equipos
                jornada_goleador[jornada[i][0]] = [
                    dict_goles, dict_equipos_goleadores]

        # Visualizacion de los datos almacenados
        # Recorremos todas las jornadas
        for jornada in jornada_goleador:
            # Si se selecciona una jornada, solo muestra esa jornada, sino muestra todas. Por defecto va a mostrar todas.
            if jornada == mostrar_jornada or mostrar_jornada == '':
                print('\n')
                # Mostramos la jornada
                print(self.color_nombre(jornada))
                # Separamos los datos de la jornada
                datos_jornada = jornada_goleador[jornada]
                # Los goles en una variable
                gol = datos_jornada[0]["Cantidad_de_goles"]
                # Los equipos en otra, ordenados alfabeticamente ascendente
                equipos = sorted(datos_jornada[1]["equipos"])
                # Mostramos los goles
                print(f'Cantidad maxima de goles de la jornada: {self.descripcion_color(gol)}')

                # Diferenciamos si es un equipo o varios
                if len(equipos) == 1:
                    print('El equipo goleador es: ')
                else:
                    print('Los equipos goleadores son: ')

                # Le damos formato de equipo, equipo, equipo, etc...
                cont = 0
                for equipo in equipos:
                    if cont == 0:
                        print(self.descripcion_color(equipos[cont]), end='')
                        cont += 1
                    else:
                        print(',', self.descripcion_color(equipos[cont]), end='')
                        cont += 1

        print('')

        # Devolvemos los resultados para realizar de ser necesario, el grafico.
        return jornada_goleador

    # Equipo con mas puntos en el campeonato.
    # Como parametros indicamos si se visualiza los datos en la terminal o no. Por defecto no se muestra
    def query_equipo_puntero(self, terminal=False):
        # La tabla la ordenamos segun del puntos totales de forma descendiente
        query_puntero = self.query_tabla_posiciones('Puntos desc')

        # Configuramos para que muestre el equipo puntero
        resultado = self.select(query_puntero, 'fetchone')
        conexion = sqlite3.connect('torneo_argentino.db')
        df = pd.read_sql_query(query_puntero, conexion)
        
         # Damos a elegir si se quiere mostrar por terminal
        if terminal:
            print(f'''
El equipo puntero del campeonato es {self.color_nombre(resultado[0].upper())}.
Con {self.descripcion_color(resultado[8])} puntos y {self.descripcion_color(resultado[1])} partidos jugados, de los cuales: 
- Ganó {self.descripcion_color(resultado[2])} 
- Empató {self.descripcion_color(resultado[3])}
- Perdió {self.descripcion_color(resultado[4])}
Convirtió {self.descripcion_color(resultado[5])} goles y le hicieron {self.descripcion_color(resultado[6])}.
		    ''')
            print(f'\n{self.color_nombre("TABLA DE POSICIONES COMPLETA")}\n')
            print(self.tabla_color(df.head(28)))
            print('')

        # Devolvemos los resultados para realizar de ser necesario, el grafico.
        return df

    # Equipo mas goleador
    # Como parametros indicamos si se visualiza los datos en la terminal o no. Por defecto no se muestra
    def query_equipos_goleador(self, terminal=False):
        # Configuramos para que muestre el equipo con mas goles
        query_goleador = self.query_tabla_posiciones('GF desc')
        resultado = self.select(query_goleador, 'fetchone')
        conexion = sqlite3.connect('torneo_argentino.db')
        df = pd.read_sql_query(query_goleador, conexion)

         # Damos a elegir si se quiere mostrar por terminal
        if terminal:
            print(f'''
El equipo goleador del campeonato es {self.color_nombre(resultado[0].upper())}.
Con {self.descripcion_color(resultado[5])} goles convertidos.
            ''')
            print(f'\n{self.color_nombre("TABLA DE POSICIONES (Los 5 mejores)")}\n')
            print(self.tabla_color(df.head(5)))
            print('')

        # Devolvemos los resultados para realizar de ser necesario, el grafico.
        return df

    # Equipo con mas victorias de local.
    # Como parametros indicamos si se visualiza los datos en la terminal o no. Por defecto no se muestra
    def query_mas_ganador_local(self, terminal=False):
        # Contamos los resultados solamente de los que se jugaron de forma local
        query_local_ganador = '''SELECT * , sum(GF)-sum(GC) as GT,
					sum(PG*3 + PE) as Puntos, ROUND(CAST(PG AS FLOAT)/PJ,2)*100 as "Promedio PG/PJ"
				from (
					SELECT equipo as Equipo,  
						sum( case when "equipo_local" = "equipo" THEN 1 
						else 0 end) as PJ,
						sum(case when "goles_local" > "goles_visitante" THEN 1 
						else 0 end) as PG,
						sum(case when "goles_local" = "goles_visitante" THEN 1 
						else 0 end) as PE,
						sum(case when "goles_local" < "goles_visitante" THEN 1 
						else 0 end) as PP,
						sum(goles_local) as GF,
						sum(goles_visitante) as GC
					FROM equipos_2022 
					INNER JOIN temporada_2022 
						on equipo = equipo_local
					GROUP by equipo
					)
				group by equipo
				ORDER by "Promedio PG/PJ" desc '''

        resultado = self.select(query_local_ganador, 'fetchone')
        conexion = sqlite3.connect('torneo_argentino.db')
        df = pd.read_sql_query(query_local_ganador, conexion)

        # Damos a elegir si se quiere mostrar por terminal
        if terminal:
            print(f'''
El equipo con mayor cantidad de partidos ganados de local es {self.color_nombre(resultado[0].upper())}.
Con {self.descripcion_color(resultado[2])} partidos ganados entre {self.descripcion_color(resultado[1])} partidos disputados.
Su promedio fue de {self.descripcion_color(resultado[9])} % de efectividad de local
            ''')
            print(f'\n{self.color_nombre("TABLA DE POSICIONES (Los 5 mejores)")}\n')
            print(self.tabla_color(df.head(5)))
            print('')

        # Devolvemos los resultados para realizar de ser necesario, el grafico.
        return df

    # Script para la tabla de goles por jornada
    def query_goles_jornada(self, terminal=False):
        query = '''SELECT jornada as Jornada,  SUM(goles_local) as 'Goles Local', sum(goles_visitante) 'Goles Visitante', SUM(goles_local+goles_visitante) as 'Total de goles'
                FROM temporada_2022
                GROUP BY jornada
                ORDER BY CAST(SUBSTR(Jornada, 9) as UNSIGNED INTEGER)
                '''

        conexion = sqlite3.connect('torneo_argentino.db')
        df = pd.read_sql_query(query, conexion)
        # Damos a elegir si se quiere mostrar por terminal
        if terminal:
            print(f'\n{self.tabla_color(df)}')

        # Devolvemos los resultados para realizar los gráficos
        return df

    def query_equipo_perdedor(self, terminal=False):
        # La tabla la ordenamos segun del puntos totales de forma ascendiente
        query_puntero = self.query_tabla_posiciones('Puntos asc')

        # Configuramos para que muestre el equipo con menos puntos
        resultado = self.select(query_puntero, 'fetchone')
        conexion = sqlite3.connect('torneo_argentino.db')
        df = pd.read_sql_query(query_puntero, conexion)

        # Damos a elegir si se quiere mostrar por terminal
        if terminal:
            print(f'''
El equipo con menos puntos del campeonato es {self.color_nombre(resultado[0].upper())}.
Con {self.descripcion_color(resultado[8])} puntos y {self.descripcion_color(resultado[1])} partidos jugados, de los cuales: 
- Ganó {self.descripcion_color(resultado[2])} 
- Empató {self.descripcion_color(resultado[3])}
- Perdió {self.descripcion_color(resultado[4])}
Convirtió {self.descripcion_color(resultado[5])} goles y le hicieron {self.descripcion_color(resultado[6])}.
            ''')
            print(f'\n{self.color_nombre("TABLA DE POSICIONES (Los 5 peores)")}\n')
            print(self.tabla_color(df.head(5)))
            print('')

        # Devolvemos los resultados para realizar de ser necesario, el grafico.
        return df

    def query_goles_contra(self, terminal=False):
        query = '''
				SELECT equipo as Equipo, SUM(case when equipos_2022.equipo = temporada_2022.equipo_local then goles_visitante else goles_local end) as "Goles en contra"
				FROM equipos_2022 INNER JOIN temporada_2022
				WHERE equipos_2022.equipo = temporada_2022.equipo_local OR equipos_2022.equipo = temporada_2022.equipo_visitante
				group by equipo
				ORDER BY "Goles en contra" desc
				'''

        resultado = self.select(query, 'fetchone')
        conexion = sqlite3.connect('torneo_argentino.db')
        df = pd.read_sql_query(query, conexion)

        # Damos a elegir si se quiere mostrar por terminal
        if terminal:
            print(
                f'\nEl equipo que recibió más goles es: {self.color_nombre(resultado[0].upper())}, con un total de {self.descripcion_color(resultado[1])} goles.')

            print(f'\n{self.color_nombre("TABLA DE POSICIONES (Los 5 peores)")}\n')
            print(self.tabla_color(df.head(5)))
            print('')

        return df

    # Script para obtener el equipo con más victorias de visitante

    def query_victorias_visitante(self, terminal=False):
        # PVV: promedio de victorias como visitante; VV: victorias visitantes
        query = '''
			SELECT equipo as Equipo, victorias_visitantes as VV, PJ, (ROUND(CAST(victorias_visitantes AS FLOAT)/PJ,2))*100 as PVV
			FROM ( SELECT  equipo, sum(case when goles_visitante > goles_local then 1 else 0 end) as victorias_visitantes, sum(case when equipos_2022.equipo = temporada_2022.equipo_visitante then 1 else 0 end) as PJ
					FROM equipos_2022 INNER JOIN temporada_2022
					WHERE equipos_2022.equipo = temporada_2022.equipo_visitante
					GROUP BY equipo
					ORDER BY victorias_visitantes desc
			)
			ORDER BY PVV desc
		'''
        resultado = self.select(query, 'fetchone')

        conexion = sqlite3.connect('torneo_argentino.db')
        df = pd.read_sql_query(query, conexion)

        # Damos a elegir si se quiere mostrar por terminal
        if terminal:
            print(f'''
El equipo con más victorias de visitantes es {self.color_nombre(resultado[0].upper())}
- Partidos jugados de visitante: {self.descripcion_color(resultado[2])}
- Partidos ganados: {self.descripcion_color(resultado[1])}
- Su promedio es de {self.descripcion_color(resultado[3])}% de efectividad de visitante.
                ''')
            print(f'\n{self.tabla_color("TABLA DE POSICIONES (Los 5 mejores)")}\n')
            print(self.tabla_color(df.head(5)))
            print('')

        return df

    def color_nombre(self,nombre):
        coloreado = "\033[4;36m" + str(nombre) + "\033[0;m"
        return coloreado

    def descripcion_color(self, descripcion):
        coloreado = "\033[1;31m" + str(descripcion) + "\033[0;m"
        return coloreado
    
    def tabla_color(self, tabla):
        coloreado = "\033[1;33m" + str(tabla) + "\033[0;m"
        return coloreado
