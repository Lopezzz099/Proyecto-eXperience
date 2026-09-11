from datos import DIAS, EDIFICIOS, OBJETIVOS, crear_matriz
from operaciones import (
    validar_edificio, validar_semana, validar_dia, validar_valor, validar_mes, validar_menu,
    registrar_datos, total_semana, total_mensual, semana_completa,
    contar_cumplimiento_por_semana, cumplimiento_semana, buscar_edificio,
    porcentaje_cumplimiento, promedio_diario_semana, promedio_semanal_edificio,
    dia_extremo, top_semanas, dia_extremo_periodo,
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

# Item 3
def indicadores_semanales(matrices):
    semana = input("Semana a consultar (1-4): ")
    while not (semana.isdigit() and validar_semana(int(semana))):
        print("Semana inválida.")
        semana = input("Semana a consultar (1-4): ")
    semana = int(semana) - 1

    for indice in range(len(EDIFICIOS)):
        matriz = matrices[indice]
        objetivo = OBJETIVOS[indice]
        print(f"{EDIFICIOS[indice]}:")
        if semana_completa(matriz, semana):
            total = total_semana(matriz, semana)
            promedio_diario = promedio_diario_semana(matriz, semana)
            promedio_semanal = promedio_semanal_edificio(matriz)
            porcentaje = porcentaje_cumplimiento(matriz, semana, objetivo)
            print(f"  Total semanal: {total} kWh")
            print(f"  Promedio diario: {promedio_diario:.2f} kWh")
            print(f"  Promedio semanal del edificio: {promedio_semanal:.2f} kWh")
            print(f"  Cumplimiento: {porcentaje:.2f} %")

            extremo = dia_extremo(matriz, semana)
            if extremo is not None:
                valor_max, nombres_max, valor_min, nombres_min = extremo
                texto_max = ""
                for nombre in nombres_max:
                    texto_max = texto_max + nombre + "; "
                texto_min = ""
                for nombre in nombres_min:
                    texto_min = texto_min + nombre + "; "
                print(f"  Día de mayor generación: {valor_max} kWh ({texto_max})")
                print(f"  Día de menor generación: {valor_min} kWh ({texto_min})")
        else:
            print("  Semana incompleta, no se puede calcular.")

# Item 4
def alerta_semana_puntual(matrices, semana):
    for indice in range(len(EDIFICIOS)):
        matriz = matrices[indice]
        objetivo = OBJETIVOS[indice]
        cumplio = cumplimiento_semana(matriz, semana, objetivo)
        print(f"{EDIFICIOS[indice]}:")
        if cumplio is None:
            print("  Semana incompleta, no se puede verificar.")
        elif cumplio:
            print("  Cumplió el objetivo semanal.")
        else:
            print("  Producción inferior al objetivo semanal. Se recomienda realizar una revisión.")

def informe_cumplimiento_periodo(matrices):
    for indice in range(len(EDIFICIOS)):
        cumplieron, no_cumplieron = contar_cumplimiento_por_semana(matrices[indice], OBJETIVOS[indice])
        print(f"{EDIFICIOS[indice]}: {cumplieron} semanas cumplidas, {no_cumplieron} no cumplidas.")

def alertas_cumplimiento(matrices):
    semana = input("Semana a verificar (1-4): ")
    while not (semana.isdigit() and validar_semana(int(semana))):
        print("Semana inválida.")
        semana = input("Semana a verificar (1-4): ")
    semana = int(semana) - 1

    alerta_semana_puntual(matrices, semana)
    print("Resumen del período:")
    informe_cumplimiento_periodo(matrices)

# Item 5
def informe_ranking_top3(matrices):
    for indice in range(len(EDIFICIOS)):
        matriz = matrices[indice]
        print(f"{EDIFICIOS[indice]}:")
        top3 = top_semanas(matriz, 3)
        if len(top3) < 3:
            print(f"  Aviso: solo hay {len(top3)} semanas completas disponibles.")
        print("  Ranking (Top 3 semanas):")
        for semana, total in top3:
            print(f"    Semana {semana + 1}: {total} kWh")

def informe_extremos(matrices):
    for indice in range(len(EDIFICIOS)):
        matriz = matrices[indice]
        print(f"{EDIFICIOS[indice]}:")

        resultado_dia = dia_extremo_periodo(matriz)
        if resultado_dia is None:
            print("  Sin datos suficientes para calcular el día extremo.")
        else:
            valor_max, ubicaciones_max, valor_min, ubicaciones_min = resultado_dia
            texto_max = ""
            for semana, dia in ubicaciones_max:
                texto_max = texto_max + f"Semana {semana + 1} - {dia}; "
            texto_min = ""
            for semana, dia in ubicaciones_min:
                texto_min = texto_min + f"Semana {semana + 1} - {dia}; "
            print(f"  Día de mayor generación: {valor_max} kWh ({texto_max})")
            print(f"  Día de menor generación: {valor_min} kWh ({texto_min})")

        resultado_semana = semana_extremo_periodo(matriz)
        if resultado_semana is None:
            print("  Sin semanas completas para calcular la semana extremo.")
        else:
            valor_max, semanas_max, valor_min, semanas_min = resultado_semana
            texto_max = ""
            for semana in semanas_max:
                texto_max = texto_max + f"Semana {semana + 1}; "
            texto_min = ""
            for semana in semanas_min:
                texto_min = texto_min + f"Semana {semana + 1}; "
            print(f"  Semana de mayor generación: {valor_max} kWh ({texto_max})")
            print(f"  Semana de menor generación: {valor_min} kWh ({texto_min})")

def informe_comparacion(matrices):
    total_a, total_b = total_periodo_comparable(matrices[0], matrices[1])
    valor_max, edificios_max, valor_min, edificios_min = edificio_extremo(total_a, total_b)
    texto_max = ""
    for edificio in edificios_max:
        texto_max = texto_max + edificio + "; "
    texto_min = ""
    for edificio in edificios_min:
        texto_min = texto_min + edificio + "; "
    print(f"  Mayor generación acumulada: {valor_max} kWh ({texto_max})")
    print(f"  Menor generación acumulada: {valor_min} kWh ({texto_min})")

def rankings(matrices):
    informe_ranking_top3(matrices)
    informe_extremos(matrices)
    print("Comparación entre edificios:")
    informe_comparacion(matrices)

# Item 6
def informe_resumen_mensual(matrices, mes):
    print(f"Resumen del mes: {mes}")
    for indice in range(len(EDIFICIOS)):
        matriz = matrices[indice]
        total = total_mensual(matriz)
        promedio = promedio_semanal_edificio(matriz)
        print(f"{EDIFICIOS[indice]}:")
        print(f"  Total generado en el mes: {total} kWh")
        if promedio is None:
            print("  Promedio semanal: sin semanas completas para calcularlo.")
        else:
            print(f"  Promedio semanal: {promedio:.2f} kWh")

def informes(matrices, mes):
    print("1. Informe semanal por edificio")
    print("2. Comparación entre edificios")
    print("3. Cumplimiento de objetivos")
    print("4. Ranking / Top 3 de semanas")
    print("5. Máximos y mínimos")
    print("6. Resumen mensual")
    sub_opcion = input("Elija una opción: ")

    if sub_opcion == "1":
        consultar_edificio(matrices)
    elif sub_opcion == "2":
        informe_comparacion(matrices)
    elif sub_opcion == "3":
        informe_cumplimiento_periodo(matrices)
    elif sub_opcion == "4":
        informe_ranking_top3(matrices)
    elif sub_opcion == "5":
        informe_extremos(matrices)
    elif sub_opcion == "6":
        informe_resumen_mensual(matrices, mes)
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
                indicadores_semanales(matrices)
            elif opcion == 4:
                alertas_cumplimiento(matrices)
            elif opcion == 5:
                rankings(matrices)
            elif opcion == 6:
                informes(matrices, mes)
            elif opcion == 7:
                salir = True
        else:
            print("Opción inválida.")