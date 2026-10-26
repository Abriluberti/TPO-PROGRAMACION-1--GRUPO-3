
AGUA_SIN_EXPLORAR = 0
NAVE_OCULTA = 1
AGUA_MARCADA = 2
IMPACTO = 3
HUNDIDO = 4
DETECTADO_SONAR = 5


def buscar_lineal(cubo, estado_buscado=NAVE_OCULTA):
    """Busca en el cubo todas las celdas con un estado dado.

    Recibe:
        cubo: lista de listas de listas de tamaño N x N x N.
        estado_buscado: estado de celda a localizar.

    Devuelve:
        Una tupla con la lista de puntos encontrados y sus métricas.

    Excepciones:
        No lanza excepciones propias.
    """
    n = len(cubo)

    puntos = []
    comparaciones = 0

    for z in range(n):
        for y in range(n):
            for x in range(n):
                comparaciones += 1

                if cubo[z][y][x] == estado_buscado:
                    puntos.append((z + 1, x + 1, y + 1))

    metricas = {
        "comparaciones": comparaciones,
        "tiempo_ms": 0.0,
        "profundidad_max": 0
    }

    return puntos, metricas