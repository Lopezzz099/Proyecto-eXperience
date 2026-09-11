from datos import DIAS, MESES, EDIFICIOS, OBJETIVOS, crear_matriz
from operaciones import (
    validar_edificio, validar_semana, validar_dia, validar_valor, validar_mes, validar_menu,
    registrar_datos, total_semana, total_mensual, semana_completa,
    contar_cumplimiento_por_semana, cumplimiento_semana, buscar_edificio,
    porcentaje_cumplimiento, promedio_diario_semana, promedio_semanal_edificio,
    dia_extremo, ranking_semanas, top_semanas, dia_extremo_periodo,
    semana_extremo_periodo, total_periodo_comparable, edificio_extremo,
    generar_datos_random, datos_edificio
)

def pedir_mes():
    mes = input("Ingrese el mes de análisis: ")
    while not validar_mes(mes):
        print("Mes inválido.")
        mes = input("Ingrese el mes de análisis: ")
    return mes

# Item 2 del menu
def consultar_edificio(matrices):
    codigo = input("Código de edificio (ED-A / ED-B): ")
    if not validar_edificio(codigo):
        print("Código de edificio inválido.")
        return

    matriz, objetivo = datos_edificio(matrices, codigo)

    for semana in range(len(matriz)):
        print(f"Semana {semana + 1}:")
        if semana_completa(matriz, semana):
            total = total_semana(matriz, semana)
            promedio = promedio_diario_semana(matriz, semana)
            porcentaje = porcentaje_cumplimiento(matriz, semana, objetivo)
            print(f"  Total: {total} kWh")
            print(f"  Promedio diario: {promedio:.2f} kWh")
            print(f"  Cumplimiento: {porcentaje:.2f} %")
        else:
            print("  Semana incompleta, no se puede calcular.")

# Item 1 del menu el cual tiene dos subItems
def registrar_o_generar(matrices):
    print("1. Cargar dato manualmente")
    print("2. Generar datos aleatorios para ambos edificios")
    sub_opcion = input("Elija una opción: ")

    if sub_opcion == "1":
        codigo = input("Código de edificio (ED-A / ED-B): ")
        while not validar_edificio(codigo):
            print("Código inválido.")
            codigo = input("Código de edificio (ED-A / ED-B): ")
        indice = buscar_edificio(codigo)

        semana = input("Semana (1-4): ")
        while not (semana.isdigit() and validar_semana(int(semana))):
            print("Semana inválida.")
            semana = input("Semana (1-4): ")
        semana = int(semana) - 1

        dia = input("Día (Lunes a Viernes): ")
        while not validar_dia(dia):
            print("Día inválido.")
            dia = input("Día (Lunes a Viernes): ")
        dia = DIAS.index(dia.lower().title())

        valor = input("Energía generada (kWh): ")
        while not (valor.isdigit() and validar_valor(int(valor))):
            print("Valor inválido.")
            valor = input("Energía generada (kWh): ")
        valor = int(valor)

        registrar_datos(matrices[indice], semana, dia, valor)
        print("Dato registrado correctamente.")

    elif sub_opcion == "2":
        generar_datos_random(matrices[0])
        generar_datos_random(matrices[1])
        print("Datos aleatorios generados para ambos edificios.")

    else:
        print("Opción inválida.")

def main():
    matrices = [crear_matriz(), crear_matriz()]
    mes = pedir_mes()
    salir = False

    while not salir:
        print("1. Registrar/actualizar generación")
        print("2. Consultar edificio")
        print("3. Indicadores semanales")
        print("4. Alertas de cumplimiento")
        print("5. Rankings")
        print("6. Informes")
        print("7. Salir")
        opcion = input("Elija una opción: ")

        if opcion.isdigit() and validar_menu(int(opcion)):
            opcion = int(opcion)
            if opcion == 1:
                registrar_o_generar(matrices)
            elif opcion == 2:
                consultar_edificio(matrices)
            elif opcion == 3:
                pass
            elif opcion == 4:
                pass
            elif opcion == 5:
                pass
            elif opcion == 6:
                pass
            elif opcion == 7:
                salir = True
        else:
            print("Opción inválida.")