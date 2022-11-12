from inicio import InicioMain
import time

def main():
    comenzar=InicioMain()
    print(f"\n{comenzar.advertencia_color('Por favor, corrobore que tiene instaladas las versiones de los módulos que figuran en el archivo:')}\n{comenzar.link_color('requirements.txt')}")
    try:
        time.sleep(2)
        arranque=input(f'\nDesea continuar ({comenzar.opcion_color("s/n")}): ')
        if arranque[0].upper()=='S':
            comenzar.dialogo()
        else:
            raise KeyError
    except Exception:
        comenzar.despedida()
  
if __name__ == '__main__':
    main()

