
AGUA_SIN_EXPLORAR = 0
NAVE_OCULTA = 1
AGUA_MARCADA = 2
IMPACTO = 3
HUNDIDO = 4
DETECTADO_SONAR = 5


def buscar_lineal(cubo, estado_buscado=NAVE_OCULTA):
    n = len(cubo)

    puntos = []
    comparaciones = 0

    for z in range(n):
        for x in range(n):
            for y in range(n):
                comparaciones += 1
                if cubo[z][x][y] == estado_buscado:
                    puntos.append((z + 1, x + 1, y + 1))

    metricas = {
        "comparaciones": comparaciones,
    }
    return puntos, metricas