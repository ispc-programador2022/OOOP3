from agregar_datos import Agregar
from scraper import Scraper
from script_sql import Bbdd
from consultas_sql import ConsultasSQL
import time
import os
from random import randrange

class InicioMain():
    def __init__(self):
        self.usuario = input("\nPor favor antes de comenzar ingrese su nombre: ")

    def dialogo(self):
        time.sleep(1)
        print(f"\nBIENVENID@ {self.usuario.upper()}. \nESTA ES UNA SIMPLE APP QUE REALIZAMOS ENTRE MARTINA OCTTINGER Y MARTIN ARIEL OLLER.")
        time.sleep(2)
        try:
            intro=input(f'\n{self.usuario.title()} quieres leer una breve descripción del trabajo que realizamos. (s/n): ')
        except Exception:
            print(f'Por un error tendremos que finalizar la app. Lo sientimos {self.usuario.capitalize()}\n')
             
        else:
            while True:
                if intro[0].upper() == 'N':
                    self.iniciar_datos()
                    break
                elif intro[0].upper() == 'S':

                    print("\nPara lograr el objetivo de nuestro proyecto integrador con scrapping, python y bases de datos,\n")
                    time.sleep(3)

                    print("cada integrante eligió un tema y sorteamos uno, que usamos para este trabajo.\n")
                    time.sleep(3)

                    print("En un principio eramos 3 integrantes, pero lamentablemente Brian, no pudo seguir con el proyecto.\n")
                    time.sleep(3)

                    print("El tema sorteado fue sobre resultados de futbol. Investigamos un par de webs donde desarrollar web scrapping, y dimos con la indicada: https://ar.marca.com/claro/futbol/primera-division/fixture.html\n")
                    time.sleep(3)
                    
                    print("De aquí extrajimos los resultados y equipos de cada partido, en cada una de las jornadas, del torneo argentino de fútbol de primera división de la temporada 2022.\n")
                    time.sleep(3)
                
                    print("Con estos datos creamos varias tablas, como tabla general, goles por equipos, goles por jornada, y otras más.\n")
                    time.sleep(3)

                    print("A continuación, los dejamos con las opciones de visualización: por terminal, gráficos en un dashboard o ambos.\n")
                    time.sleep(3)
                    self.iniciar_datos()
                    break
                else:
                    intro=input(f'\nPor favor, {self.usuario.title()} solo tenemos 2 opciones, "s" para si o "n" para no. (s/n): ')

            visual=input(f'''
    {self.usuario.title()} elige entre estas opciones de visualización de nuestro trabajo: 
    - Op. "T" = Verlo por la terminal
    - Op. "D" = Ver las gráficas en el Dashboard
    - Op. "S" = Salir
    ''')
            while True:
                if visual[0].upper()== "T":
                    opcion = self.opciones_terminal()
                    self.datos_terminal(opcion)
                    continuar=input(f"\n{self.usuario.title()} querés continuar con alguna otra visualización (s/n): ")
                    if continuar[0].upper() == 'N':
                        visual=input(f'''
    {self.usuario.title()} elige entre estas opciones de visualización de nuestro trabajo: 
    - Op. "T" = Verlo por la terminal
    - Op. "D" = Ver las gráficas en el Dashboard
    - Op. "S" = Salir
    ''')
                        continue
                    elif continuar[0].upper() == 'S':
                        visual='T'
                        continue
                    else:
                        continuar=input(f'Por favor {self.usuario.title()}, confirma con "s" continuar con alguna otra visualización, o con "n" para salir (s/n): ')

                elif visual[0].upper() == "D":
                    
                    try:
                        print('\nEl dashboard se abrirá en tu explorador predeterminado.\n')
                        print('Para salir del servidor, combina las teclas "Crtl"+"C".\n')
                        os.system("python dashboard.py")
                    except KeyboardInterrupt:
                        print('\nServer web finalizada')
                    continuar=input(f"\n{self.usuario.title()} querés continuar con alguna otra visualización (s/n): ")
                    if continuar[0].upper() == 'N':
                        break
                    elif continuar[0].upper() == 'S':
                        visual=input(f'''
    {self.usuario.title()} elige entre estas opciones de visualización de nuestro trabajo: 
    - Op. "T" = Verlo por la terminal
    - Op. "D" = Ver las gráficas en el Dashboard
    - Op. "S" = Salir
    ''')
                        continue
                    else:
                        continuar=input(f'Por favor {self.usuario.title()}, confirma con "s" continuar con alguna otra visualización, o con "n" para salir (s/n): ')
                elif visual[0].upper()  == "S":
                    break  

                else:
                    visual=input(f'{self.usuario.title()} las opciones son "T" o "D" o "S": ')

        finally:
            self.despedida()



    def iniciar_datos(self):
        print(f'\nEsto va a demorar un poco {self.usuario.title()}, si es la primera vez que se ingresan los datos. ')
        bd = Bbdd()
        bd.iniciar()
        bd.crear_tabla()
        url = 'https://ar.marca.com/claro/futbol/primera-division/fixture.html'

        s1 = Scraper(url)
        contenido = s1.parser()
        filas = s1.extraer(contenido)

        agregar = Agregar(bd, filas)
        agregar.agregar_datos()

    def opciones_terminal(self):
        print(
"""
Para la ejecución en terminal te adjuntamos las opciones disponibles:
1 - Equipo puntero
2 - Cantidad de victorias y empates
3 - Promedios de victorias y empates
4 - Equipo goleador de la jornada
5 - Goles totales por jornada
6 - Equipo goleador
7 - Equipo con mas goles en contra
8 - Equipo con mas victorias de local
9 - Equipo con mas victorias de visitante
10 - Último de la tabla""")
        try:
            opcion=int(input('Ingresa el número de la tabla, para ver tu consulta (1 - 10): '))
            if opcion > 0 and opcion <= 10:
                return opcion
            else:
                print(f'Solo se perpiten opciones del 1 al 10 {self.usuario.capitalize()}. Por defecto mostraremos una tabla al azar.\n')
                opcion=randrange(1,11)
                return opcion
        except ValueError:
            print(f'Solo se perpiten opciones numericas {self.usuario.capitalize()}. Por defecto mostraremos una tabla al azar.\n')
            opcion=randrange(1,11)
            return opcion
        

    def datos_terminal(self, opcion):
        csql=ConsultasSQL()
        terminal=True
        if opcion == 1:
            csql.query_equipo_puntero(terminal)
        elif opcion == 2:
            csql.query_resultados(terminal)
        elif opcion == 3:
            csql.query_promedio_resultados(terminal)
        elif opcion == 4:
            try:
                jornada = int(input('\nIngrese una jornada de la 1 a la 27: '))
                if jornada > 0 and jornada <= 27:
                    mostrar = f'Jornada {jornada}'
                    csql.query_mas_goles_jornada(mostrar)
                else:
                    print('Lamentablemente no existe esa jornada, por lo que te mostraremos el listado completo.\n\nQue lo disfrutes!!!!!')
                    csql.query_mas_goles_jornada()
            except Exception:
                print('Lamentablemente no existe esa jornada, por lo que te mostraremos el listado completo.\n\nQue lo disfrutes!!!!!')
                csql.query_mas_goles_jornada()
        elif opcion == 5:
            csql.query_goles_jornada(terminal)
        elif opcion == 6:
            csql.query_equipos_goleador(terminal)
        elif opcion == 7:
            csql.query_goles_contra(terminal)
        elif opcion == 8:
            csql.query_mas_ganador_local(terminal)
        elif opcion == 9:
            csql.query_victorias_visitante(terminal)
        elif opcion == 10:
            csql.query_equipo_perdedor(terminal)
        print('')

    def despedida(self):
        print(f'\nMuchas gracias {self.usuario.capitalize()} por su visita. Espero haya sido de su agrado nuestra app.\n\nHasta  la próxima.')
    

