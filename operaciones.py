# VALIDACIONES

from datos import DIAS, OBJETIVOS, MESES, EDIFICIOS, crear_matriz

def validar_edificio(codigo):
    return codigo in EDIFICIOS

def validar_semana(semana):
    return semana in (1, 2, 3, 4)

def validar_dia(dia):
    return dia in DIAS or (type(dia) == int and 1 <= dia <= 5)
