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