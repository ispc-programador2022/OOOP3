from agregar_datos import Agregar
from scraper import Scraper
from script_sql import Bbdd


def main():
    bd = Bbdd()
    bd.iniciar()
    bd.crear_tabla()
    url = 'https://ar.marca.com/claro/futbol/primera-division/fixture.html'

    s1 = Scraper(url)
    contenido = s1.parser()
    filas = s1.extraer(contenido)

    agregar = Agregar(bd, filas)
    agregar.agregar_datos()


if __name__ == '__main__':
    main()
