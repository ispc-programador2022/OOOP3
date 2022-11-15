 #Librería para corroborar las versiones de los paquetes instalados
from importlib_metadata import PackageNotFoundError, version
import time
import os


def main():
    try:
        avanzar = revision_paquetes()
        if avanzar[0] == True:
            if avanzar[1] == 'Nada':
                from inicio import InicioMain
                comenzar=InicioMain(False)
                comenzar.dialogo()
            else:
                from inicio import InicioMain
                comenzar=InicioMain(True)
                comenzar.dialogo()
        else:
            time.sleep(1)
            print('\nAdiós\n')
    except ModuleNotFoundError as e:
            print(f'No está instalado el módulo de {e.name}')
            time.sleep(2)
            print(f'\nPara utilizar esta app, necesita tener instalados los paquetes de que figuran en el archivo requirements.txt')
            print(f'Puede usar el comando pip install -r requirements.txt, para instalar y/o actualizar todos los paquetes, o realizarlo de forma manual')
            
def revision_paquetes():
    requerimientos=open('requirements.txt')
    avanzar = False
    paquete_instalado = 'Nada'
    for linea in requerimientos.readlines():
        linea_reque=linea
        paquete=linea[:linea_reque.find('=')]
        version_reque=linea[linea_reque.rfind('=')+1:].replace('\n','')
        try:
            if version_reque.replace('.','') > version(paquete).replace('.',''):
                print(f'\nHabría que actualizar {paquete.upper()}, su version es {version(paquete)} y, para evitar errores, necesitamos {version_reque}')
                seguir=input('\nDesea actualizar el paquete(s/n)? ') 
                try:
                    if seguir[0].upper()=='S'or seguir.upper()=='S':
                        time.sleep(1)
                        print('\nLa instalación puede demorar unos instantes. Aguarde por favor...\n')
                        time.sleep(1)
                        os.system(f"python -m pip install {paquete}")
                        time.sleep(1)
                        print(f'\nSe actualizó existosamente el paquete de {paquete.upper()}.')
                        time.sleep(1)
                        avanzar = True
                        paquete_instalado = paquete
                    else:
                        avanzar = False
                        break
                except Exception:
                    print('\nOpción no valida. Cerraremos la app')
                    avanzar= False
                    break
            else:
                avanzar = True
        except PackageNotFoundError as e:
            print(f'\nNo está instalado el paquete de {e.name.upper()}')
            try:
                time.sleep(1)
                instalar=input(f'Desea instalar el paquete {e.name.upper()} (s/n): ')
                if instalar[0].upper() == 'S' or instalar.upper() == 'S':
                    time.sleep(1)
                    print('\nLa instalación puede demorar unos instantes. Aguarde por favor...\n')
                    time.sleep(1)
                    os.system(f"python -m pip install {e.name}")
                    time.sleep(1)
                    print(f'\nSe instaló existosamente el paquete de {e.name.upper()}.')
                    time.sleep(1)
                    avanzar = True
                    paquete_instalado = e.name
                else:
                    avanzar = False
            except Exception:
                print('\nOpción no valida. Cerraremos la app')
                time.sleep(1)
                print(f'\nPuede usar el comando pip install -r requirements.txt, para instalar y/o actualizar todos los paquetes, para utilizar está app.')
                avanzar= False
                break
        else:
            avanzar= True
    return avanzar , paquete_instalado
        

if __name__ == '__main__':
    main()

