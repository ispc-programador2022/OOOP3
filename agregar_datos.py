import threading


class Agregar:
    # bd = base de datos ya creada
    # filas = datos ya extraidos con el scraper
    def __init__(self, bd, filas):
        self.bd = bd
        self.filas = filas

    def agregar_datos(self):
        query = '''INSERT INTO temporada_2022 VALUES (null, ?,?,?,?,?)'''
        print('Se estan agregando datos a la tabla. Aguarde unos instantes...')

        for fila in self.filas:
            try:
                self.bd.insert_delete_update(query, (fila.jornada, fila.local, fila.resultado_local,
                                                    fila.visitante, fila.resultado_visitante))
            except Exception:
                print('Ya estan agregados los datos en la tabla')
                break
            
                                             
        print('Se completó con existo la carga.\n')