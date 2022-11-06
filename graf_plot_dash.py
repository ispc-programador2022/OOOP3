from consultas_sql import ConsultasSQL
from dash import Dash,dcc
import dash_bootstrap_components as dbc
import plotly.express as px


class Plot_dash():
    def __init__(self):    
        self.titulo=[
           'Top 5 de equipos con más goles convertidos',
           'Top 5 de equipos con más goles en contra',
           'Top 5 de equipos más efectivos de local', 
           'Top 5 de equipos más efectivos de visitante',
           'Total de goles por jornada', 
        ]
        self.ejes_x=["Equipo","Jornada"]
        self.titulo_eje_x=["EQUIPO","JORNADA"]
        self.ejes_y=["GF","Goles en contra","Promedio PG/PJ","PVV","Total goles"]
        self.titulo_eje_y=['GOLES',"PROMEDIO PG/PJ"]
        
    def config_grafico(self,df,filas,titulo,ejes_x,ejes_y,rango,titulo_eje_x,titulo_eje_y):
        app = Dash(__name__)

        df=df.head(filas)

        fig = px.bar(df, x=ejes_x, y=ejes_y, color=ejes_y, range_color=rango, color_continuous_scale="Rainbow")

        fig.update_layout(barmode='relative',xaxis=dict(title_text = titulo_eje_x), yaxis=dict(title_text = titulo_eje_y))

        app = Dash(external_stylesheets=[dbc.themes.FLATLY])
        app.layout = dbc.Container([
           
            dbc.CardBody(f'{titulo}', style={'color': '#a58ccd', 'fontSize': 32,'font-family':'Calibri',},),

            dbc.CardBody(dcc.Graph(
                id='torneo_argentino_2022',
                figure=fig
            ))
        ])

        if __name__ == '__main__':
            app.run_server(debug=True)

    def grafico(self,opcion_grafico=1):
        try:
            consulta = ConsultasSQL()

            if opcion_grafico == 1:
                df = consulta.query_equipos_goleador()
                max=int(df[self.ejes_y[0]].max().max())+5
                min=int(df[self.ejes_y[0]].min().min())-5
                self.config_grafico(df,5,self.titulo[0],self.ejes_x[0],self.ejes_y[0],[min,max],self.titulo_eje_x[0],self.titulo_eje_y[0])

            elif opcion_grafico == 2:
                df = consulta.query_goles_contra()
                max=int(df[self.ejes_y[1]].max().max())+5
                min=int(df[self.ejes_y[1]].min().min())-5
                self.config_grafico(df,5,self.titulo[1],self.ejes_x[0],self.ejes_y[1],[min,max],self.titulo_eje_x[0],self.titulo_eje_y[0])

            elif opcion_grafico == 3:
                df = consulta.query_mas_ganador_local()
                max=int(df[self.ejes_y[2]].max().max())+5
                min=int(df[self.ejes_y[2]].min().min())-5
                self.config_grafico(df,5,self.titulo[2],self.ejes_x[0],self.ejes_y[2],[min,max],self.titulo_eje_x[0],self.titulo_eje_y[1])

            elif opcion_grafico == 4:
                df = consulta.query_victorias_visitante()
                max=int(df[self.ejes_y[3]].max().max())+5
                min=int(df[self.ejes_y[3]].min().min())-5
                self.config_grafico(df,5,self.titulo[3],self.ejes_x[0],self.ejes_y[3],[min,max],self.titulo_eje_x[0],self.titulo_eje_y[1])

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