
AGUA_SIN_EXPLORAR = 0
NAVE_OCULTA = 1
AGUA_MARCADA = 2
IMPACTO = 3
HUNDIDO = 4
DETECTADO_SONAR = 5


def buscar_lineal(cubo, estado_buscado=NAVE_OCULTA):
    """Busca en el cubo todas las celdas con un estado dado (método lineal).
 
    Recorre las N*N*N celdas con tres ciclos for anidados, sin estructuras
    auxiliares para decidir: solo se usa una lista donde se acumulan los
    hallazgos.
 
    Recibe:
        cubo: lista de listas de listas (N x N x N), creada por tablero.py.
        estado_buscado: estado de celda a localizar. Por defecto NAVE_OCULTA.
    Devuelve:
        Una tupla (puntos, metricas).
        puntos: lista de tuplas (z, x, y), con valores de 1 a N, en el
            orden en que fueron encontradas.
        metricas: diccionario con las claves "comparaciones" (int),
            "tiempo_ms" (float) y "profundidad_max" (int). El tiempo queda en
            0.0 por ahora. La profundidad vale 0 porque este método no es
            recursivo.
    Lanza:
        No lanza excepciones propias. Si el cubo no es una matriz anidada
        N x N x N, Python puede lanzar TypeError o IndexError.
    """
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