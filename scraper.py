import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url):
        self.url = url

    def parser(self):
        r = requests.get(self.url)
        contenido = BeautifulSoup(r.text, 'html.parser')
        return contenido

    def extraer(self, contenido):
        # Traigo todas las tablas (27)
        jornadas = contenido.find_all('table', class_='jor agendas')

        for jornada in jornadas:
            # Obtengo el nombre de cada jornada
            jornadaNum = jornada.find('caption').text
            print(f'\n\n{jornadaNum}\n{"-"*35}')

            # Busco el cuerpo de la tabla, donde se encuentra la información que necesitamos, luego obtengo todas las filas
            for equipos in jornada.find_all('tbody'):
                rows = equipos.find_all('tr')

                # Itero cada fila y guardo en variables la información que va a ir en la base de datos
                for row in rows:
                    local = row.find('td', class_='local').text.strip()
                    resultado = row.find('td', class_='resultado').text.strip()
                    visitante = row.find('td', class_='visitante').text.strip()

                    # Separo el resultado de local y el resultado de visitante
                    if len(resultado) == 3:
                        resultadoLocal = resultado[0]
                        resultadoVisitante = resultado[2]
                    else:
                        resultadoLocal = '-'
                        resultadoVisitante = '-'

                    print(
                        f'{local}({resultadoLocal})   {resultado}   {visitante}({resultadoVisitante})')
