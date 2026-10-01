def crear_cubo(n=8):
    """
    Crea un cubo de n x n x n celdas.

    Recibe:
        n: tamaño del cubo.

    Devuelve:
        Un cubo representado como una lista de listas de listas.
    """

    cubo = []

    for z in range(n):
        capa = []

        for y in range(n):
            fila = []

            for x in range(n):
                fila.append("~")

            capa.append(fila)

        cubo.append(capa)

    return cubo


def punto_valido(punto, n):
    """
    Verifica si un punto pertenece al cubo.

    El punto debe estar formado por z, x, y,
    con valores entre 1 y n.

    Recibe:
        punto: tupla con las coordenadas (z, x, y).
        n: tamaño del cubo.

    Devuelve:
        True si el punto es válido.
        False si está fuera del cubo.
    """

    z, x, y = punto

    return (
        1 <= z <= n
        and 1 <= x <= n
        and 1 <= y <= n
    )


def dibujar_plano_z(cubo, z):
    """
    Dibuja una capa del cubo fijando el valor de z.

    Recibe:
        cubo: cubo de juego.
        z: número de la capa que se quiere dibujar.

    Devuelve:
        Un texto con la representación del plano.
    """

    plano = cubo[z - 1]

    dibujo = f"========= CAPA z = {z} =========\n"

    dibujo += "    "

    for x in range(1, len(plano[0]) + 1):
        dibujo += f"x{x} "

    dibujo += "\n"

    for y in range(len(plano)):
        dibujo += f"y{y + 1}  "

        for x in range(len(plano[y])):
            dibujo += f"{plano[y][x]}  "

        dibujo += "\n"

    return dibujo


def sumar_matrices(a, b):
    """
    Suma dos matrices del mismo tamaño.

    Recibe:
        a: primera matriz.
        b: segunda matriz.

    Devuelve:
        La matriz resultante.
    """

    resultado = []

    for i in range(len(a)):
        fila = []

        for j in range(len(a[i])):
            fila.append(a[i][j] + b[i][j])

        resultado.append(fila)

    return resultado


def restar_matrices(a, b):
    """
    Resta dos matrices del mismo tamaño.

    Recibe:
        a: primera matriz.
        b: segunda matriz.

    Devuelve:
        La matriz resultante.
    """

    resultado = []

    for i in range(len(a)):
        fila = []

        for j in range(len(a[i])):
            fila.append(a[i][j] - b[i][j])

        resultado.append(fila)

    return resultado


def multiplicar_matrices(a, b):
    """
    Multiplica dos matrices compatibles.

    Recibe:
        a: primera matriz.
        b: segunda matriz.

    Devuelve:
        La matriz resultante.
    """

    filas_a = len(a)
    columnas_a = len(a[0])
    columnas_b = len(b[0])

    resultado = []

    for i in range(filas_a):
        fila = []

        for j in range(columnas_b):
            acumulador = 0

            for k in range(columnas_a):
                acumulador += a[i][k] * b[k][j]

            fila.append(acumulador)

        resultado.append(fila)

    return resultado


def transponer_matriz(matriz):
    """
    Obtiene la matriz transpuesta.

    Recibe:
        matriz: matriz original.

    Devuelve:
        La matriz transpuesta.
    """

    filas = len(matriz)
    columnas = len(matriz[0])

    resultado = []

    for j in range(columnas):
        fila = []

        for i in range(filas):
            fila.append(matriz[i][j])

        resultado.append(fila)

    return resultado