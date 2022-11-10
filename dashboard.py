import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html, dash_table
from dash.dependencies import Output, Input, State
from consultas_sql import ConsultasSQL
from graficos import Graficos

consulta = ConsultasSQL()
grafico = Graficos()
lista_equipos = consulta.query_equipo_puntero().loc[:, 'Equipo']

# APP -------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.FONT_AWESOME],
                meta_tags=[
    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
)

# LAYOUT del dashboard: Dash-Bootstrap-Components
# -------------------------------------------------------
app.layout = dbc.Container([
    dbc.Row([
        # # *-*-*-*-*-*-*-*-* HEADER *-*-*-*-*-*-*-*-*
        dbc.Col([
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/YO1impuFJT2hex6wvCd9Pw_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/wi-J-3U7th2bpIB_Uy9Euw_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/700Mj6lUNkbBdvOVEbjC3g_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/BXhsD_6yvgePrhCIeziDcA_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/3arLHe5K6lOpRpQhi2_WDQ_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/3guH9PUqsLcUw9o8VBhAlw_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/NBOwSdURT-K9-F5z2yhgjA_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/_Vs9SZ4f9XZbgLC2ee_GTA_48x48.png',
                width='25px'
            ),
            html.Img(
                src='//ssl.gstatic.com/onebox/media/sports/logos/RjY9F3KQksU2z_ce3iE7dQ_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/uomxa4z3oGOtwEcHoAJdFQ_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/Lss4UJ_IL6ekpEzz1hYKug_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/u9y68E7VuYQeNAVLB-8HBw_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/MW12yOtJtAqfvt7JKt4iUg_48x48.png',
                width='25px'
            ),


        ], width=3),
        dbc.Col([
            html.H1("Torneo Argentino de Fútbol 2022",
                    className='text-center text-light fw-bold fs-2'),
            html.Span(
                'Info',
                className='badge rounded-pill bg-secondary',
                id='popover-target',
                n_clicks=0,
                style={'width': '25%'}),
            # # *-*-*-*-*-*-*-*-* POPOVER *-*-*-*-*-*-*-*-*
            dbc.Popover([
                dbc.PopoverHeader('Sobre la Primera División'),
                dbc.PopoverBody(
                    'La Primera División de Argentina es el torneo de la primera categoría del fútbol masculino argentino, organizado desde 1893 por la Asociación del Fútbol Argentino. Los nuevos participantes fueron los dos equipos ascendidos de la Primera Nacional 2021: Tigre, que regresó tras su última participación en la temporada 2018-19, y Barracas Central, que formó parte de la categoría después de haberlo hecho por última vez en 1934, en la era amateur. INICIO: 3 de Junio 2022. CIERRE: 25 de Octubre 2022'
                )
            ], id='popover', target='popover-target', is_open=False, placement='right', trigger="click"),
            html.Span(
                'Tabla de posiciones',
                id='open-xl',
                className='badge rounded-pill bg-secondary',
                style={'width': '25%', 'margin-top': '5px'}),
            # # *-*-*-*-*-*-*-*-* MODAL *-*-*-*-*-*-*-*-*
            dbc.Modal([
                dbc.ModalHeader(
                    dbc.ModalTitle("Tabla de posiciones")
                ),
                dbc.ModalBody(
                    dash_table.DataTable(
                        consulta.query_equipo_puntero().to_dict('records'),
                        [
                            {"name": i, "id": i} for i in consulta.query_equipo_puntero().columns
                        ],
                        virtualization=True,
                        page_action='none',
                        style_header={
                            'backgroundColor': '#212529',
                            'fontWeight': 'bold',
                            'color': 'white'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#f8f9fa',
                            },
                        ]
                    )
                ),
            ],
                id="modal-xl",
                size="xl",
                is_open=False,
            ),
        ], width=6, class_name='d-flex align-items-center', style={'flex-direction': 'column '}),
        # # *-*-*-*-*-*-*-*-* ICONOS DE LOS EQUIPOS *-*-*-*-*-*-*-*-*
        dbc.Col([
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/YkuS0LD4UowC0MDzpKqZXw_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/8amyvPwO0h6V9D_U2NdG_g_48x48.png',
                width='25px'
            ),
            # html.Img(
            #     src='https://dimg-pa.googleapis.com/lg/CgYwMDAwMDA.png?sig=AJweQhU6_f56AgDt7pYXqm1a6FJS&key=AIzaSyCUqbG5Kw_8jb3cy2ZBKvV2kAi8z0qmQO0&sk=r7Evjfpq7nk&w=48&h=48',
            #     width='25px'
            # ),
            # html.Img(
            #     src='https://www.gstatic.com/onebox/sports/logos/inverse-crest.svg',
            #     width='25px'
            # ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/nDfL4YLZSNWXZniXushVag_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/M5i5Qs9SCl8wGOmvMI7Giw_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/z-n52o4GCyVOhf7N_VRMBw_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/tDd7ZfndQ-Z5PI3sOiBkNQ_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/2QDTzVrXBo6JHyEdqWj5Hw_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/7Q4qedU_pq59ZYez21HyMA_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/lRUvM7_5xXHy2h9wohKZ9A_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/YGkWVpsFb9FS1WRxl8ZdWg_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/EG7pVKQAW2mvbnKsMoMbYA_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/FiqktuVwEcYAOZNp32H-OQ_48x48.png',
                width='25px'
            ),
            html.Img(
                src='https://ssl.gstatic.com/onebox/media/sports/logos/XRBWSDuC8J2bANaRlbvyHA_48x48.png',
                width='25px'
            ),

        ], width=3, class_name='align-items-center'),
    ], align='center', class_name='  py-5 text-white bg-primary rounded-3 mb-3'
    ),
    # # *-*-*-*-*-*-*-*-* FIN HEADER *-*-*-*-*-*-*-*-*

    # # *-*-*-*-*-*-*-*-* FILA 1, GRAFICOS 1 - 3 *-*-*-*-*-*-*-*-*
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(children=[
                    dcc.Dropdown(id='my-dpdn', multi=False, value='5 Equipos goleadores',
                                    options=['5 Equipos goleadores', '5 Equipos más goleados'], className='text-dark')
                ], class_name='bg-primary'),
                dbc.CardBody(
                    dcc.Graph(id='bar-fig', figure={})
                )

            ])
        ],  width={'size': 6, 'offset': 0},
        ),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Partidos Jugados',
                                       class_name='bg-primary text-light'),
                        dbc.CardBody(consulta.query_resultados().iat[0, 0] + consulta.query_resultados(
                        ).iat[0, 1] + consulta.query_resultados().iat[0, 2], className='justify-content-center d-flex fs-2 fw-bold text-primary')
                    ], class_name='card border-primary'),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Victorias Locales',
                                       class_name='bg-primary text-light'),
                        dbc.CardBody(consulta.query_resultados(
                        ).iat[0, 0], className='justify-content-center d-flex fs-2 fw-bold text-primary')
                    ], class_name='card border-primary'),
                ]),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Victorias Visitantes',
                                       class_name='bg-primary text-light'),
                        dbc.CardBody(consulta.query_resultados(
                        ).iat[0, 1], className='justify-content-center d-flex fs-2 fw-bold text-primary')
                    ], class_name='card border-primary')

                ]),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(
                            'Empates', class_name='bg-primary text-light'),
                        dbc.CardBody(consulta.query_resultados(
                        ).iat[0, 2], className='justify-content-center d-flex fs-2 fw-bold text-primary')
                    ], class_name='card border-primary')

                ])
            ], className='my-2'),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=grafico.grafico(
                        3), className='py-0')
                ])
            ])

        ],  width=6,
        ),
    ],  align='start'),
    # # *-*-*-*-*-*-*-*-* FILA 2, GRAFICOS 4 - 5 *-*-*-*-*-*-*-*-*
    dbc.Row([
        dbc.Col([
            dbc.Card(
                [
                    dcc.Graph(figure=grafico.grafico(4))
                ]
            )
        ], width={'size': 5, 'offset': 0}),
        dbc.Col([
            dbc.Card([
                dcc.Graph(figure=grafico.grafico(5))
            ])

        ], width={'size': 7, 'offset': 0}),

    ], justify='start', align='center'),

    # # *-*-*-*-*-*-*-*-* FILA 3, GRAFICOS 6 - 7 *-*-*-*-*-*-*-*-*
    dbc.Card([
        dbc.CardHeader([
            'Seleccione el/los equipos que desee comparar:',
            dcc.Dropdown(id='dpdn_equipos', multi=True, value=['Boca Juniors', 'River Plate', 'Racing Club', 'Huracán', 'Banfield'],
                            options=[{'label': x, 'value': x}
                                     for x in sorted(lista_equipos.unique())],
                            className='text-primary'),
        ], class_name='col-12 bg-primary text-light'),
        dbc.CardBody([
            dcc.Graph(id='ef_l', figure={},
                      className='col-6 border border-primary'),
            dcc.Graph(id='ef_v', figure={},
                      className='col-6 border border-primary')

        ], class_name='col-12 d-flex justify-content-between', style={'flex-direction': 'row'})

    ], class_name=' card my-3'),

    # # *-*-*-*-*-*-*-*-* FOOTER *-*-*-*-*-*-*-*-*
    html.Footer([
                html.Div(children=[
                    html.Span([

                        html.A('ISPC', href='https://www.ispc.edu.ar/',
                               target='_blank', className='text-light fw-bold'),
                        html.P(' - Proyecto Integrador 2022 - Gamma - OOOP3',
                               className='text-light')
                    ], className='d-flex', style={'gap': '10px'}),
                    html.P('Martín Oller - Martina Octtinger'),
                    html.Div([
                        html.I(
                            className="fa-brands fa-github"),
                        html.A(
                            'Github', href='https://github.com/ispc-programador2022/OOOP3', target='_blank', className='text-light')
                    ],
                        style={
                        'display': 'flex', 'align-items': 'center', 'gap': '10px'}, className='fs-5')
                ],

                    style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'width': '100%'}),

                ], className='text-light bg-primary rounded-3 mt-5 p-5')

], fluid=True, class_name='px-5')


# # *-*-*-*-*-*-*-*-* CALLBACKS *-*-*-*-*-*-*-*-*
# **************************
# MODAL - Tabla de posiciones - *Se abre la tabla de posiciones al apretar el botón*


@app.callback(
    Output("modal-xl", "is_open"),
    Input("open-xl", "n_clicks"),
    State("modal-xl", "is_open"),
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Gráfico 1 y 2 - 5 más goleadores/ 5 más goleados - Gráfico de barras


@app.callback(
    Output('bar-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(seleccion):
    if seleccion == '5 Equipos goleadores':
        grafico_1 = grafico.grafico(1)
    elif seleccion == '5 Equipos más goleados':
        grafico_1 = grafico.grafico(2)
    return grafico_1

# Grafico 6 - Eficacia Local - Bar chart - multiple


@app.callback(
    Output('ef_l', 'figure'),
    Input('dpdn_equipos', 'value')
)
def update_graph(lst_eq):
    df = grafico.grafico(6)
    df = df[df.index.isin(lst_eq)]
    grafico_6 = px.bar(
        data_frame=df,
        text='value',
        title='Eficacia como Local',
        color_discrete_sequence=['#30123b', '#3f8ef5']
    )
    return grafico_6

# Grafico 7 - Eficacia visitante - Bar chart - multiple


@app.callback(
    Output('ef_v', 'figure'),
    Input('dpdn_equipos', 'value')
)
def update_graph(lst_eq):
    df = grafico.grafico(7)
    df = df[df.index.isin(lst_eq)]
    grafico_7 = px.bar(
        data_frame=df,
        text='value',
        title='Eficacia como Visitante',
        color_discrete_sequence=['#30123b', '#3f8ef5'])
    return grafico_7


# # *-*-*-*-*-*-*-*-* RUN APP *-*-*-*-*-*-*-*-*

if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
