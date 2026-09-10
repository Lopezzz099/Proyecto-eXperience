# Tuplas
DIAS = ("Lunes", "Martes", "Miercoles", "Jueves", "Viernes")
EDIFICIOS = ("ED-A", "ED-B")
OBJETIVOS = (1000, 800)
MESES = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")

# Genero la matriz para semana x dia con valores iniciales en -1
def crear_matriz():
    return [[-1 for i in range(5)] for i in range(4)]