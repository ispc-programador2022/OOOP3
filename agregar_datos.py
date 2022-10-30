class Agregar:
    # bd = base de datos ya creada
    # filas = datos ya extraidos con el scraper
    def __init__(self, bd, filas):
        self.bd = bd
        self.filas = filas

    def agregar_datos(self):
        query = '''INSERT INTO temporada_2022 VALUES (null, ?,?,?,?,?)'''

        for fila in self.filas:
            self.bd.insert_delete_update(query, (fila.jornada, fila.local, fila.resultado_local,
                                                 fila.visitante, fila.resultado_visitante))
