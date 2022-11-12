from agregar_datos import Agregar
from scraper import Scraper
from script_sql import Bbdd
from consultas_sql import ConsultasSQL
import time
import os
from random import randrange
from colorama import Fore

class InicioMain():
    def __init__(self):
        self.usuario = input("\nHOLA! Antes de comenzar ingrese su nombre: ")
        

    def dialogo(self):
        time.sleep(1)
        print(f"\nBIENVENID@ {self.color_nombre(self.usuario.upper())}. \nESTA ES UNA SIMPLE APP QUE REALIZAMOS ENTRE {self.color_nombre('MARTINA OCTTINGER')} Y {self.color_nombre('MARTIN ARIEL OLLER')}.")
        time.sleep(2)
        try:
            intro=input(f'\n{self.color_nombre(self.usuario.title())} quieres leer una breve descripción del trabajo que realizamos ({self.opcion_color("s/n")}): ')
        except Exception:
            print(f'Por un error tendremos que finalizar la app. Lo sientimos {self.color_nombre(self.usuario.capitalize())}\n')
             
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

                    print(f"El tema sorteado fue sobre resultados de futbol. Investigamos un par de webs donde desarrollar web scrapping, y dimos con la indicada: {self.link_color('https://ar.marca.com/claro/futbol/primera-division/fixture.html')}\n")
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
                    intro=input(f'\nPor favor, {self.color_nombre(self.usuario.title())} solo tenemos 2 opciones, "s" para si o "n" para no ({self.opcion_color("s/n")}): ')

            visual=input(f'''
    {self.color_nombre(self.usuario.title())} elige entre estas opciones de visualización de nuestro trabajo: 
    - Op. {self.opcion_color('"T"')} = {self.descripcion_color("Verlo por la terminal")}
    - Op. {self.opcion_color('"D"')} = {self.descripcion_color("Ver las gráficas en el Dashboard")}
    - Op. {self.opcion_color('"S"')} o tecla {self.opcion_color('"ENTER"')}  = {self.descripcion_color("Salir")} 
    ''')
            while True:
                try:
                    if visual[0].upper()== "T":
                        opcion = self.opciones_terminal()
                        self.datos_terminal(opcion)
                        continuar=input(f'\n{self.color_nombre(self.usuario.title())} querés continuar con alguna otra visualización ({self.opcion_color("s/n")}): ')
                        if continuar[0].upper() == 'N':
                            visual=input(f'''
    {self.color_nombre(self.usuario.title())} elige entre estas opciones de visualización de nuestro trabajo: 
    - Op. {self.opcion_color('"T"')} = {self.descripcion_color("Verlo por la terminal")}
    - Op. {self.opcion_color('"D"')} = {self.descripcion_color("Ver las gráficas en el Dashboard")}
    - Op. {self.opcion_color('"S"')} o tecla {self.opcion_color('"ENTER"')}  = {self.descripcion_color("Salir")} 
    ''')
                            continue
                        elif continuar[0].upper() == 'S':
                            visual='T'
                            continue
                        else:
                            continuar=input(f'Por favor {self.color_nombre(self.usuario.title())}, confirma con "s" continuar con alguna otra visualización, o con "n" para salir ({self.opcion_color("s/n")}): ')

                    elif visual[0].upper() == "D":

                        try:
                            print(f'\nEl dashboard se abrirá en tu explorador predeterminado,\npara ello, combina las teclas {self.opcion_color("Ctrl")} + {self.opcion_color("clic izquierdo")} sobre el vinculo del servidor que aparecerá abajo.\n')
                            
                            print(f'Para salir del servidor, combina las teclas {self.opcion_color("Ctrl + C")}.\n')
                            print(Fore.BLUE)
                            os.system("python dashboard.py")
                        except KeyboardInterrupt:
                            print(Fore.RESET+f'\n{self.advertencia_color("Server web finalizada")}')
                        continuar=input(f'\n{self.color_nombre(self.usuario.title())} querés continuar con alguna otra visualización ({self.opcion_color("s/n")}): ')
                        if continuar[0].upper() == 'N':
                            break
                        elif continuar[0].upper() == 'S':

                            visual=input(f'''
    {self.color_nombre(self.usuario.title())} elige entre estas opciones de visualización de nuestro trabajo: 
    - Op. {self.opcion_color('"T"')} = {self.descripcion_color("Verlo por la terminal")}
    - Op. {self.opcion_color('"D"')} = {self.descripcion_color("Ver las gráficas en el Dashboard")}
    - Op. {self.opcion_color('"S"')} o tecla {self.opcion_color('"ENTER"')}  = {self.descripcion_color("Salir")}
    ''')
                            continue
                        else:
                            continuar=input(f'Por favor {self.color_nombre(self.usuario.title())}, confirma con "s" continuar con alguna otra visualización, o con "n" para salir ({self.opcion_color("s/n")}): ')
                    elif visual[0].upper()  == "S":
                        break  

                    else:
                        visual=input(f'{self.color_nombre(self.usuario.title())} las opciones son "T" o "D" o "S": ')
        
                except Exception as e:
                    break
            
        finally:
            self.despedida()



    def iniciar_datos(self):
        print(f'\nEsto va a demorar un poco {self.color_nombre(self.usuario.title())}, si es la primera vez que se ingresan los datos. ')
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
    f"""
    Para la ejecución en terminal te adjuntamos las opciones disponibles:
    {self.opcion_color('1')} - {self.descripcion_color('Equipo puntero')}
    {self.opcion_color('2')} - {self.descripcion_color('Cantidad de victorias y empates')}
    {self.opcion_color('3')} - {self.descripcion_color('Promedios de victorias y empates')}
    {self.opcion_color('4')} - {self.descripcion_color('Equipo goleador de la jornada')}
    {self.opcion_color('5')} - {self.descripcion_color('Goles totales por jornada')}
    {self.opcion_color('6')} - {self.descripcion_color('Equipo goleador')}
    {self.opcion_color('7')} - {self.descripcion_color('Equipo con mas goles en contra')}
    {self.opcion_color('8')} - {self.descripcion_color('Equipo con mas victorias de local')}
    {self.opcion_color('9')} - {self.descripcion_color('Equipo con mas victorias de visitante')}
    {self.opcion_color('10')} - {self.descripcion_color('Último de la tabla')}""")
        try:
            opcion=int(input(f'Ingresa el número de la tabla, para ver tu consulta {self.opcion_color("1 - 10")}: '))
            if opcion > 0 and opcion <= 10:
                return opcion
            else:
                print(f'Solo se perpiten opciones del 1 al 10 {self.color_nombre(self.usuario.capitalize())}. Por defecto mostraremos una tabla al azar.\n')
                opcion=randrange(1,11)
                return opcion
        except ValueError:
            print(f'Solo se perpiten opciones numericas {self.color_nombre(self.usuario.capitalize())}. Por defecto mostraremos una tabla al azar.\n')
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
                jornada = int(input(f'\nIngrese una jornada de la {self.opcion_color("1")} a la {self.opcion_color("27")}: '))
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
        print(f'\nMuchas gracias {self.color_nombre(self.usuario.capitalize())} por su visita. Espero haya sido de su agrado nuestra app.\n\n{self.advertencia_color("Hasta la próxima.")}\n')
    

    def color_nombre(self,nombre):
        coloreado = "\033[3;36m" + str(nombre) + "\033[0;m"
        return coloreado

    def opcion_color(self, opcion):
        coloreado = "\033[1;35m" + str(opcion) + "\033[0;m"
        return coloreado

    def descripcion_color(self, descripcion):
        coloreado = "\033[1;32m" + str(descripcion) + "\033[0;m"
        return coloreado

    def link_color(self, link):
        coloreado = "\033[4;34m" + str(link) + "\033[0;m"
        return coloreado

    def advertencia_color(self, advertencia):
        coloreado = "\033[1;31m" + str(advertencia) + "\033[0;m"
        return coloreado