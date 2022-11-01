from itertools import count
import sqlite3
from script_sql import Bbdd
import pandas as pd

class ConsultasSQL(Bbdd):
	def __init__(self):
		self.iniciar()
		self.tabla_equipos()

	#Creamos una tabla con los equipos, para utilizarlo en futuros filtros de las las tablas
	def tabla_equipos(self):
		query_equipos='''CREATE TABLE IF NOT EXISTS equipos_2022 as
						SELECT DISTINCT(equipo_local)as equipo 
						FROM temporada_2022 
						ORDER BY equipo'''
		self.cursor.execute(query_equipos)
		self.conexion.commit()
		self.conexion.close()

	#Script para la tabla de posiciones completa, con el campo de "ORDER BY" con la posibilidad de modificarlo para diferentes consultas. Por defecto la tabla está ordenada por los puntos totales en orden descendiente
	def query_tabla_posiciones(self, order_by= 'Puntos desc'):
		#Se realiza la union de 2 tablas la de visitante y local sumando los totales de cada columna
		#NOMENCLATURA: PJ:partidos jugados, PG:partidos ganados, PE:partidos empatados, PP:partidos perdidos, 
		#	GF:goles a favor, GC:goles en contra, GT: diferencia de goles entre a favor y en contra, 
		#	Puntos:Total de puntos obtenidos (3 puntos por cada PG, 1 punto por cada PE)
		query =f'''SELECT equipo as Equipo, sum(PJ) as PJ, sum(PG) PG, sum(PE) PE, sum(PP) PP, sum(GF) GF, sum(GC) GC , sum(GF)-sum(GC) as GT,
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

	#Promedio de resultados 
	#Definimos la fucion con el parametro "Formato" para que nos muestre con que opción mostrar los resultados de la consulta
	# Por defecto el parametro va a ser como tabla.
	def query_promedio_resultados(self, tabla=False):
		#Se realiza el conteo de partidos ganados de local, visitante y empates y se los divide por el total de partidos
		#Para que nos de como resultado números decimales en lugar de dividir por 100, realizamos la multiplicación por 0.01 y todo eso lo redondeamos a 2 valores decimales
		query='''SELECT count(jornada) as "Cantidad de partidos",
		round(sum(CASE  WHEN "goles_local" > "goles_visitante" THEN 1 ELSE 0 END) / (count(jornada)*0.01),2) as "Porcentaje Victorias Locales",
		round(sum(CASE  WHEN "goles_local" < "goles_visitante" THEN 1 ELSE 0 END) / (count(jornada)*0.01),2) as "Porcentaje Victorias Visitante",
		round(sum(CASE  WHEN "goles_local" = "goles_visitante" THEN 1 ELSE 0 END)/ (count(jornada)*0.01),2) as "Porcentaje Empates"
		FROM temporada_2022'''
		resultados=self.select(query,'fetchone') #fetchone porque solo vamos a tener una lista de elementos

		#Para aplicar Pandas se utiliza la funcion read_sql_query, y para ello necesitamos el parametro con los datos de conexión por ello es que lo formulamos en la variable conexion.
		conexion=sqlite3.connect('torneo_argentino.db')
		df=pd.read_sql_query(query,conexion)
		
		print('')
		index=0
		for i in df:
			if index==0:
				print(f'\t - {i} = {resultados[index]}')
				index +=1
			else:
				print(f'\t - {i} = {resultados[index]} %')
				index +=1
		print('')
		
		if tabla:
		#Se imprime los datos de la tabla con Pandas
			print('\n',df,'\n')
		
		#Devolvemos los resultados para generar graficos de ser necesario
		return df

	#Equipo goleador de la fecha
	#La función tiene como parametro "mostrar_jornada" para que se elija de que jornada visualizar los datos
	# Por defecto esta vacio que devuelve cada uan de las jornadas
	def query_mas_goles_jornada(self, mostrar_jornada=''):
		#Lista donde ingresaremos cada una de las diferentes jornadas realizadas
		lista_jornada = []
		query_jornada='''Select distinct jornada from temporada_2022 order by id'''
		self.iniciar()
		lista_jornada.append(self.select(query_jornada, 'fetchall'))
		
		#En este diccionario pondremos de cada una de las jornadas los goles maximos y cuales son los equipos que los realizaron
		jornada_goleador={}
		
		#Query para obtener el valor de gol maximo de cada jornada
		jornada_max_gol='''SELECT jornada, max(max(goles_local), max(goles_visitante)) as 'Máximo anotador de la jornada'
		FROM temporada_2022
		where jornada like ?
		GROUP by jornada
		ORDER by id'''
		
		#Query para buscar las coincidencias de cada partido segun el maximo de goles.Si no hay coicidencia devuelve NULL y despues lo eliminamos.
		query_equipo_goleador='''SELECT * from (
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

		#Recorremos el total de jornadas para crear nuestro diccionario
		for i in range(len(lista_jornada[0])):

			for jornada in lista_jornada:
				#Creamos un diccionario para los goles
				dict_goles={}
				#Creamos un diccionario para los equipos
				dict_equipos_goleadores={}
				#Como puede haber mas de un equipo ganador los pondremos en una lista
				equipo_goleador=[]
				
				
				self.iniciar()
				self.cursor.execute(jornada_max_gol,(jornada[i]))
				#en la variable almacenamos el máximo de goles de la jornada
				gol=self.cursor.fetchone()

				#Buscamos los equipos que en la jornada cumplan con el requisito				
				self.cursor.execute(query_equipo_goleador,(gol[1],gol[1],gol[1],gol[1],gol[1],gol[1],gol[1],gol[1],jornada[i][0]))
				equipos=self.cursor.fetchall()

				#En este "for" limpiamos los valores null que nos devuelve en cada no coincidencia.
				for partido in range(len(equipos)):
					for equipo in equipos[partido]:
						if equipo != None:
							#Los almacenamos en la lista que creamos anteriormente
							equipo_goleador.append(equipo)
							
				#Agregamos los goles del diccionario
				dict_goles['Cantidad_de_goles']=gol[1]
				#Agregamos los equipos al diccionario
				dict_equipos_goleadores['equipos'] = equipo_goleador
				#Agreamos la jordada y en su interior sus respectivos datos de goles y equipos
				jornada_goleador[jornada[i][0]]=[dict_goles,dict_equipos_goleadores]

		#Visualizacion de los datos almacenados
		#Recorremos todas las jornadas
		for jornada in jornada_goleador:
			#Si se selecciona una jornada, solo muestra esa jornada, sino muestra todas. Por defecto va a mostrar todas.
			if jornada == mostrar_jornada or mostrar_jornada=='':
				print('\n')
				#Mostramos la jornada
				print(jornada)
				#Separamos los datos de la jornada
				datos_jornada = jornada_goleador[jornada]
				#Los goles en una variable
				gol=datos_jornada[0]["Cantidad_de_goles"]
				#Los equipos en otra, ordenados alfabeticamente ascendente
				equipos=sorted(datos_jornada[1]["equipos"])
				#Mostramos los goles
				print(f'Cantidad maxima de goles de la jornada: {gol}')

				#Diferenciamos si es un equipo o varios
				if len(equipos)==1:
					print('El equipo goleador es: ')
				else:
					print('Los equipos goleadores son: ')
				
				#Le damos formato de equipo,equipo,equipo,etc...
				cont=0
				for equipo in equipos:
					if cont==0:
						print(equipos[cont], end='')
						cont+=1
					else:
						print(',',equipos[cont], end='')
						cont+=1

		print('\n')

		#Devolvemos los resultados para realizar de ser necesario, el grafico.
		return jornada_goleador
		

	#Equipo con mas puntos en el campeonato.
	#Como parametros indicamos si se visualiza la tabla completa o no. Por defecto no se muestra
	def query_equipo_puntero(self,tabla=False):
		#La tabla la ordenamos segun del puntos totales de forma descendiente
		query_puntero=self.query_tabla_posiciones('Puntos desc')

		#Configuramos para que muestre el equipo puntero
		resultado= self.select(query_puntero, 'fetchone')
		print (f'''
			El equipo puntero del campeonato es {resultado[0].upper()}.
			Con {resultado[8]} puntos y {resultado[1]} partidos jugados, de los cuales: 
			- Ganó {resultado[2]} 
			- Empató {resultado[3]}
			- Perdió {resultado[4]}
			Convirtió {resultado[5]} goles y le hicieron {resultado[6]}.
		''')

		conexion=sqlite3.connect('torneo_argentino.db')
		df = pd.read_sql_query(query_puntero,conexion)
		#Damos a elegir si se quiere mostrar la tabla
		if tabla:
			print('\nTABLA DE POSICIONES COMPLETA\n')
			print(df.head(27))
			print('\n')
			
		#Devolvemos los resultados para realizar de ser necesario, el grafico.
		return df

	#Equipo mas goleador
	#Como parametros indicamos si se visualiza la tabla completa o no. Por defecto no se muestra
	def query_equipos_goleador(self,tabla=False):
		#Configuramos para que muestre el equipo con mas goles
		query_goleador=self.query_tabla_posiciones('GF desc')
		resultado= self.select(query_goleador, 'fetchone')
		print (f'''
			El equipo goleador del campeonato es {resultado[0].upper()}.
			Con {resultado[5]} goles convertidos.
		''')

		conexion=sqlite3.connect('torneo_argentino.db')
		df = pd.read_sql_query(query_goleador,conexion)

		#Damos a elegir si se quiere mostrar la tabla
		if tabla:
			print('\nTABLA DE POSICIONES COMPLETA\n')
			print(df.head(27)) 
			print('\n')

		#Devolvemos los resultados para realizar de ser necesario, el grafico.
		return df

	#Equipo con mas victorias de local.
	#Como parametros indicamos si se visualiza la tabla completa o no. Por defecto no se muestra
	def query_mas_ganador_local(self,tabla=False):
		#Contamos los resultados solamente de los que se jugaron de forma local
		query_local_ganador='''SELECT * , sum(GF)-sum(GC) as GT,
					sum(PG*3 + PE) as Puntos, ROUND(CAST(PG AS FLOAT)/PJ,2) as "Promedio PG/PJ"
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

		resultado= self.select(query_local_ganador, 'fetchone')
		print (f'''
			El equipo con mayor cantidad de partidos ganados de local es {resultado[0].upper()}.
			Con {resultado[2]} partidos ganados entre {resultado[1]} partidos disputados.
			Su promedio fue de {resultado[9]}% de efectividad de local
		''')

		conexion=sqlite3.connect('torneo_argentino.db')
		df = pd.read_sql_query(query_local_ganador,conexion)
		#Damos a elegir si se quiere mostrar la tabla
		if tabla:
			print('\nTABLA DE POSICIONES COMPLETA\n')
			print(df.head(27)) 
			print('\n') 

		#Devolvemos los resultados para realizar de ser necesario, el grafico.
		return df
		
a=ConsultasSQL()

a.query_promedio_resultados()
a.query_mas_goles_jornada('Jornada 21')
a.query_equipo_puntero()
a.query_equipos_goleador()
a.query_mas_ganador_local()
