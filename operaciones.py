# VALIDACIONES

from datos import DIAS, OBJETIVOS, MESES, EDIFICIOS, crear_matriz

def validar_edificio(codigo):
    return codigo in EDIFICIOS

def validar_semana(semana):
    return semana in (1, 2, 3, 4)

def validar_dia(dia):
    return type(dia) == str and dia.lower().title() in DIAS

def validar_valor(valor):
    return type(valor) in (int, float) and valor >= 0

def validar_mes(mes):
    return type(mes) == str and mes.lower().title() in MESES
