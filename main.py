from scraper import Scraper


def main():
    url = 'https://ar.marca.com/claro/futbol/primera-division/fixture.html'

    s1 = Scraper(url)
    contenido = s1.parser()
    s1.extraer(contenido)


if __name__ == '__main__':
    main()
