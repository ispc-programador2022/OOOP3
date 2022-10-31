from scraper import Scraper, Fila


def main():
    url = 'https://ar.marca.com/claro/futbol/primera-division/fixture.html'

    s1 = Scraper(url)
    contenido = s1.parser()
    filas = s1.extraer(contenido)

    for fila in filas:
        '''Obtengo los datos de cada fila'''
        print(fila.jornada, fila.local, fila.resultado_local,
              fila.visitante, fila.resultado_visitante)


if __name__ == '__main__':
    main()
