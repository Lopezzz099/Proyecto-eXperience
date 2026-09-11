# VALIDACIONES

from datos import DIAS, OBJETIVOS, MESES, EDIFICIOS, crear_matriz

def validar_edificio(codigo):
    return codigo in EDIFICIOS

def validar_semana(semana):
    return semana in (1, 2, 3, 4)

def validar_dia(dia):
    return type(dia) == str and dia.lower().title() in DIAS

def validar_valor(valor):
    return type(valor) in (int) and valor >= 0

def validar_mes(mes):
    return type(mes) == str and mes.lower().title() in MESES

def validar_menu(num):
    return num in (1, 2, 3, 4, 5, 6, 7)

# REGISTRAR VALOR

# Aca asumo que semana (0 - 3) y dia (0 - 4) vienen como tipo 
# numerico adaptado para la matriz.
def registrar_datos(matriz, semana, dia, valor):
    matriz[semana][dia] = valor

# CALCULOS

# Aca asumo que semana viene adaptado como valor numerico (0 - 3).
# Tambien filtro para que no cuente para la suma los valores negativos 
# de la matriz.
def total_semana(matriz, semana):
    return sum(valor for valor in matriz[semana] if valor != -1)

# Aca reutilizo total_semana que ya me daba la suma total de una semana.
def total_mensual(matriz):
    contador = 0
    for semana in range(len(matriz)):
        contador = contador + total_semana(matriz, semana)
    return contador

# Aca asumo que semana viene adaptado como valor numerico (0 - 3).
def semana_completa(matriz, semana):
    return -1 not in matriz[semana]

def contar_cumplimiento_por_semana(matriz, objetivo):
    cumplieron = 0
    no_cumplieron = 0
    # No tengo en cuenta las incompletas (semanas que tengan un -1)
    for semana in range(len(matriz)):
        if semana_completa(matriz, semana):
            if total_semana(matriz, semana) >= objetivo:
                cumplieron += 1
            else: 
                no_cumplieron += 1
    return cumplieron, no_cumplieron

def cumplimiento_semana(matriz, semana, objetivo):
    # No tengo en cuenta las incompletas (semanas que tengan un -1)
    if semana_completa(matriz, semana):
        return total_semana(matriz, semana) >= objetivo
    return None

# Devuelve la ubicacion del edificio
def buscar_edificio(codigo):
    for i in range(len(EDIFICIOS)):
        if EDIFICIOS[i] == codigo:
            return i

def porcentaje_cumplimiento(matriz, semana, objetivo):
    if semana_completa(matriz, semana):
        return (total_semana(matriz, semana) / objetivo) * 100
    return None

def promedio_diario_semana(matriz, semana):
    return total_semana(matriz, semana) / 5

def promedio_semanal_edificio(matriz):
    totales = []
    for semana in range(len(matriz)):
        if semana_completa(matriz, semana):
            totales.append(total_semana(matriz, semana))
    if not totales:
        return None
    return sum(totales) / len(totales)

# Las listas de max y min es para el caso de que haya mas de un dia con valor max.
# En caso de que todos los valores sean -1 retorna None.
# Las listas tienen el nombre del dia (texto), no la posicion.
def dia_extremo(matriz, semana):
    dias_semana = matriz[semana]
    valor_max = None
    valor_min = None
    dias_max = []
    dias_min = []
    for dia in range(len(dias_semana)):
        valor = dias_semana[dia]
        if valor != -1:
            if valor_max is None or valor > valor_max:
                valor_max = valor
                dias_max = [dia]
            elif valor == valor_max:
                dias_max.append(dia)
            if valor_min is None or valor < valor_min:
                valor_min = valor
                dias_min = [dia]
            elif valor == valor_min:
                dias_min.append(dia)
    if valor_max is None:
        return None
    nombres_max = [DIAS[dia] for dia in dias_max]
    nombres_min = [DIAS[dia] for dia in dias_min]
    return valor_max, nombres_max, valor_min, nombres_min

# Uso lambda para tomar el total de totales y asi poder decidir el orden para
# el ranking.
def ranking_semanas(matriz):
    totales = []
    for semana in range(len(matriz)):
        if semana_completa(matriz, semana):
            totales.append((semana, total_semana(matriz, semana)))
    clave = lambda item: item[1]
    for i in range(len(totales)):
        for j in range(len(totales) - 1 - i):
            if clave(totales[j]) < clave(totales[j + 1]):
                totales[j], totales[j + 1] = totales[j + 1], totales[j]
    return totales

def top_semanas(matriz, n):
    if validar_semana(n):
        return ranking_semanas(matriz)[:n]
    return None

# Aca hago algo parecido a la funcion dia_extremo pero de todo el periodo.
def dia_extremo_periodo(matriz):
    valor_max = None
    valor_min = None
    ubicaciones_max = []
    ubicaciones_min = []
    for semana in range(len(matriz)):
        for dia in range(len(matriz[semana])):
            valor = matriz[semana][dia]
            if valor != -1:
                if valor_max is None or valor > valor_max:
                    valor_max = valor
                    ubicaciones_max = [(semana, DIAS[dia])]
                elif valor == valor_max:
                    ubicaciones_max.append((semana, DIAS[dia]))
                if valor_min is None or valor < valor_min:
                    valor_min = valor
                    ubicaciones_min = [(semana, DIAS[dia])]
                elif valor == valor_min:
                    ubicaciones_min.append((semana, DIAS[dia]))
    if valor_max is None:
        return None
    return valor_max, ubicaciones_max, valor_min, ubicaciones_min

def semana_extremo_periodo(matriz):
    valor_max = None
    valor_min = None
    semanas_max = []
    semanas_min = []
    for semana in range(len(matriz)):
        if semana_completa(matriz, semana):
            total = total_semana(matriz, semana)
            if valor_max is None or total > valor_max:
                valor_max = total
                semanas_max = [semana]
            elif total == valor_max:
                semanas_max.append(semana)
            if valor_min is None or total < valor_min:
                valor_min = total
                semanas_min = [semana]
            elif total == valor_min:
                semanas_min.append(semana)
    if valor_max is None:
        return None
    return valor_max, semanas_max, valor_min, semanas_min

# Aca solo tomo solo semanas completas en ambos edificios a la vez.
def total_periodo_comparable(matriz_a, matriz_b):
    total_a = 0
    total_b = 0
    for semana in range(len(matriz_a)):
        if semana_completa(matriz_a, semana) and semana_completa(matriz_b, semana):
            total_a = total_a + total_semana(matriz_a, semana)
            total_b = total_b + total_semana(matriz_b, semana)
    return total_a, total_b

# Ahora a partir de los totales de la funcion total_periodo_comparable
# se decide cual es el mayor/menor teniendo en cuenta que puede haber
# empate. 
def edificio_extremo(total_a, total_b):
    valor_max = max(total_a, total_b)
    valor_min = min(total_a, total_b)
    edificios_max = []
    edificios_min = []
    if total_a == valor_max:
        edificios_max.append(EDIFICIOS[0])
    if total_b == valor_max:
        edificios_max.append(EDIFICIOS[1])
    if total_a == valor_min:
        edificios_min.append(EDIFICIOS[0])
    if total_b == valor_min:
        edificios_min.append(EDIFICIOS[1])
    return valor_max, edificios_max, valor_min, edificios_min

import random

def generar_datos_random(matriz, probabilidad_incompleta=0.1):
    for semana in range(len(matriz)):
        for dia in range(len(matriz[semana])):
            if random.random() < probabilidad_incompleta:
                matriz[semana][dia] = -1
            else:
                matriz[semana][dia] = random.randint(0, 1000)

def datos_edificio(matrices, codigo):
    indice = buscar_edificio(codigo)
    if indice is None:
        return None
    return matrices[indice], OBJETIVOS[indice]