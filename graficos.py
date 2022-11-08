import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px  # pip install
from consultas_sql import ConsultasSQL


class Graficos():
    def __init__(self):
        # Titulos de los distintos graficos
        self.titulo = [
            'Top 5 de equipos con más goles convertidos',
            'Top 5 de equipos con más goles en contra',
            'Efectividad de local',
            'Efectividad de visitante',
            'Total de goles por jornada',
            'Los primeros 10 equipos del torneo',
        ]

    # Función para mostar los diferentes graficos
    def grafico(self, opcion_grafico):
        try:
            # Llamamos a la clase de las consultas
            consulta = ConsultasSQL()

            # Primer gáfico es de el "Top 5 de equipos con más goles convertidos",
            if opcion_grafico == 1:
                df = consulta.query_equipos_goleador().head(5)
                grafico_1 = px.bar(
                    data_frame=df,
                    x='Equipo',
                    y='GF',
                    labels={'GF': 'Goles'},
                    title=self.titulo[0],
                    color='GF',
                    color_continuous_scale=px.colors.sequential.Turbo_r)
                return grafico_1

            #'Top 5 de equipos con más goles en contra',
            elif opcion_grafico == 2:
                df = consulta.query_goles_contra().head(5)
                # Extraemos los valores maximos y minimos de la columna para configurar los colores de grafico
                grafico_2 = px.bar(
                    data_frame=df,
                    x='Equipo',
                    y='Goles en contra',
                    labels={'Goles en contra': 'Goles'},
                    title=self.titulo[1],
                    color='Goles en contra',
                    color_continuous_scale=px.colors.sequential.Turbo_r)
                return grafico_2

            elif opcion_grafico == 3:
                # Grafico 3 -  Resultados del torneo - Pie chart
                df = consulta.query_resultados()
                df = df.T
                df.rename(columns={0: 'Total'}, inplace=True)
                grafico_3 = px.pie(
                    data_frame=df,
                    values='Total',
                    names=['Victorias Locales',
                           'Victorias Visitante', 'Empates'],
                    color_discrete_sequence=px.colors.sequential.Turbo,
                    height=300
                )
                grafico_3 = grafico_3.update_traces(textinfo='percent').update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)')
                return grafico_3

            elif opcion_grafico == 4:
                # Gráfico 4 - Goles por jornada - Gráfico de barras con animación
                df = consulta.query_goles_jornada()
                grafico_4 = px.bar(
                    data_frame=df,
                    y=['Goles Local', 'Goles Visitante'],
                    x='variable',
                    barmode='group',
                    animation_frame='Jornada',
                    range_y=[0, 30],
                    labels={'value': 'Goles', 'variable': 'Tipo'}, text='value',
                    color_discrete_sequence=px.colors.sequential.Turbo,
                    title=self.titulo[4]
                )
                grafico_4.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
                grafico_4.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500
                return grafico_4

            elif opcion_grafico == 5:
                # Grafico 5 - Primeros 10 equipos (por puntos) - Gráfico de barras
                df = consulta.query_equipos_goleador().head(10)
                grafico_5 = px.bar(
                    data_frame=df,
                    y='Puntos',
                    x='Equipo',
                    color_discrete_sequence=px.colors.sequential.Turbo_r,
                    title=self.titulo[5],
                    color='Equipo')
                return grafico_5

            #'Top 5 de equipos más efectivos de local - Bar chart - Multiple',
            elif opcion_grafico == 6:
                df = consulta.query_mas_ganador_local(
                ).loc[:, ['Equipo', 'PJ', 'PG']]
                df = df.set_index('Equipo')
                df.rename(columns={'PJ': 'Partidos Jugados',
                                   'PG': 'Partidos Ganados'}, inplace=True)
                return df

            #'Top 5 de equipos más efectivos de visitante Bar chart - Multiple',
            elif opcion_grafico == 7:
                df = consulta.query_victorias_visitante(
                ).loc[:, ['Equipo', 'PJ', 'VV']]
                df = df.set_index('Equipo')
                df.rename(columns={'PJ': 'Partidos Jugados',
                                   'VV': 'Partidos Ganados'}, inplace=True)
                return df

        except Exception as e:
            print(f'Hay un error "{e}"')
