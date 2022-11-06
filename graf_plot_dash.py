from consultas_sql import ConsultasSQL
from dash import Dash,dcc
import dash_bootstrap_components as dbc
import plotly.express as px


class Plot_dash():
    def __init__(self): 
        #Titulos de los distintos graficos   
        self.titulo=[
           'Top 5 de equipos con más goles convertidos',
           'Top 5 de equipos con más goles en contra',
           'Top 5 de equipos más efectivos de local', 
           'Top 5 de equipos más efectivos de visitante',
           'Total de goles por jornada', 
        ]
        #Nombre de las columnas de los dataframe 
        self.ejes_x=["Equipo","Jornada"]
        #Nombre del eje x para el grafico
        self.titulo_eje_x=["EQUIPO","JORNADA"]
        #Nombre de las columnas de los dataframe 
        self.ejes_y=["GF","Goles en contra","Promedio PG/PJ","PVV","Total goles"]
        #Nombre del eje y para el grafico
        self.titulo_eje_y=['GOLES',"PROMEDIO PG/PJ"]
        
    """La función tiene de parametros:
    df = DataFrame
    filas = la cantidad de filas que vamos a tomar el dataframe
    titulo = Titulos de los distintos graficos   
    ejes_x = Nombre de las columnas de los dataframe que vamos a usar en el eje x
    ejes_y = Nombre de las columnas de los dataframe que vamos a usar en el eje y
    rango = los valores maximos y minimos de las columnas del eje y
    titulo_eje_x = Nombre del eje x para el grafico
    titulo_eje_y = Nombre del eje y para el grafico
    Con esta función moldeamos los graficos
    """
    def config_grafico(self,df,filas,titulo,ejes_x,ejes_y,rango,titulo_eje_x,titulo_eje_y):
        #Definimos la variable donde insertaremos el grafico
        app = Dash(__name__)

        #Filtramos la cantidad de filas a mostrar
        df=df.head(filas)

        #Variable para la creación del gráfico
        #Los parametros que insertaremos aquí es el dataframe, que valores van en el eje x e y, y configuramos los colores a utilizar
        #Mas opciones de colores en https://plotly.com/python/builtin-colorscales/
        fig = px.bar(df, x=ejes_x, y=ejes_y, color=ejes_y, range_color=rango, color_continuous_scale="Rainbow")

        #Configuramos los titulos de cada eje 
        # barmode=Determina cómo se muestran las barras en la misma coordenada de ubicación en el gráfico. (Al final no utilice la el grafico de multiples barras)
        fig.update_layout(xaxis=dict(title_text = titulo_eje_x), yaxis=dict(title_text = titulo_eje_y))

        
        app = Dash(external_stylesheets=[dbc.themes.FLATLY])
        
        app.layout = dbc.Container([
           
            #Configuramos el titulo del grafico expuesto y en que elemento hirá situado el grafico
            #Me parecía correcto ponerlo en un cardbody, pero se puede cambiar por alguno que sea más acorde
            dbc.CardBody(f'{titulo}', style={'color': '#a58ccd', 'fontSize': 32,'font-family':'Calibri',},),

            dbc.CardBody(dcc.Graph(
                id='torneo_argentino_2022',
                figure=fig
            ))
        ])

        #Ejecutamos la app generada en el servidor
        if __name__ == '__main__':
            app.run_server()


    #Función para mostar los diferentes graficos (por defecto se muestra el primer grafico si no se elige una opción)
    # Las opciones van del 1 al 5
    def grafico(self,opcion_grafico=1):
        try:
            #Llamamos a la clase de las consultas
            consulta = ConsultasSQL()

            #Primer gáfico es de el "Top 5 de equipos con más goles convertidos",
            if opcion_grafico == 1:
                df = consulta.query_equipos_goleador()
                #Extraemos los valores maximos y minimos de la columna para configurar los colores de grafico
                max=int(df[self.ejes_y[0]].max().max())+5
                min=int(df[self.ejes_y[0]].min().min())-5
                self.config_grafico(df,5,self.titulo[0],self.ejes_x[0],self.ejes_y[0],[min,max],self.titulo_eje_x[0],self.titulo_eje_y[0])

            #'Top 5 de equipos con más goles en contra',
            elif opcion_grafico == 2:
                df = consulta.query_goles_contra()
                #Extraemos los valores maximos y minimos de la columna para configurar los colores de grafico
                max=int(df[self.ejes_y[1]].max().max())+5
                min=int(df[self.ejes_y[1]].min().min())-5
                self.config_grafico(df,5,self.titulo[1],self.ejes_x[0],self.ejes_y[1],[min,max],self.titulo_eje_x[0],self.titulo_eje_y[0])

            #'Top 5 de equipos más efectivos de local', 
            elif opcion_grafico == 3:
                df = consulta.query_mas_ganador_local()
                #Extraemos los valores maximos y minimos de la columna para configurar los colores de grafico
                max=int(df[self.ejes_y[2]].max().max())+5
                min=int(df[self.ejes_y[2]].min().min())-5
                self.config_grafico(df,5,self.titulo[2],self.ejes_x[0],self.ejes_y[2],[min,max],self.titulo_eje_x[0],self.titulo_eje_y[1])

            #'Top 5 de equipos más efectivos de visitante',
            elif opcion_grafico == 4:
                df = consulta.query_victorias_visitante()
                #Extraemos los valores maximos y minimos de la columna para configurar los colores de grafico
                max=int(df[self.ejes_y[3]].max().max())+5
                min=int(df[self.ejes_y[3]].min().min())-5
                self.config_grafico(df,5,self.titulo[3],self.ejes_x[0],self.ejes_y[3],[min,max],self.titulo_eje_x[0],self.titulo_eje_y[1])

            #'Total de goles por jornada', 
            elif opcion_grafico == 5:
                df = consulta.query_goles_jornada()
                max=int(df[self.ejes_y[4]].max().max())+5
                min=int(df[self.ejes_y[4]].min().min())-5
                print(max,min)
                self.config_grafico(df,27,self.titulo[4],self.ejes_x[1],self.ejes_y[4],[min,max],self.titulo_eje_x[1],self.titulo_eje_y[0])
        except Exception as e:
            print(f'Hay un error "{e}"')   

grafico=Plot_dash()
grafico.grafico()