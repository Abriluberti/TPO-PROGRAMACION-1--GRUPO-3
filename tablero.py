def crear_cubo(n=8):
    """Crea un cubo vacío de N×N×N celdas

    Recibe:
     tamaño del cubo.

    Devuelve:
       cubo como lista de listas de listas, celdas inicializadas con "~"

    Excepciones:
        Ninguna"""
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
    """Valida si un punto está dentro del cubo

    Recibe:
        coordenadas (z, x, y)
        tamaño del cubo

    Devuelve:
        bool: True si 1 <= z,x,y <= n. False si no

    Excepciones:
        Ninguna"""
    z, x, y = punto
    return (
            1 <= z <= n
            and 1 <= x <= n
            and 1 <= y <= n
    )


def dibujar_plano_z(cubo, z):
    """Dibuja una capa del cubo fijando el valor de z

    Recibe:
        cubo de juego
        número de la capa (1 a N)

    Devuelve:
        representación en texto del plano

    Excepciones:
        Ninguna"""
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
    """Suma dos matrices elemento a elemento

    Recibe:
      primera matriz
      segunda matriz del mismo tamaño

    Devuelve:
      matriz resultado de a + b

    Excepciones:
        Ninguna"""
    resultado = []
    for i in range(len(a)):
        fila = []
        for j in range(len(a[i])):
            fila.append(a[i][j] + b[i][j])
        resultado.append(fila)
    return resultado


def restar_matrices(a, b):
    """Resta dos matrices elemento a elemento

    Recibe:
        a (list): primera matriz
        b (list): segunda matriz del mismo tamaño

    Devuelve:
        list: matriz resultado de a - b

    Excepciones:
        Ninguna"""
    resultado = []
    for i in range(len(a)):
        fila = []
        for j in range(len(a[i])):
            fila.append(a[i][j] - b[i][j])
        resultado.append(fila)
    return resultado


def multiplicar_matrices(a, b):
    """Multiplica dos matrices compatibles

    Recibe:
        a (list): matriz de m×n
        b (list): matriz de n×p

    Devuelve:
        list: matriz resultado de m×p

    Excepciones:
        Ninguna"""
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
    """Obtiene la matriz transpuesta

    Recibe:
       matriz original

    Devuelve:
        list: matriz transpuesta

    Excepciones:
        Ninguna"""
    resultado = []
    for j in range(len(matriz[0])):
        fila = []
        for i in range(len(matriz)):
            fila.append(matriz[i][j])
        resultado.append(fila)
    return resultado


def dibujar_plano_x(cubo, x):
    """Dibuja un plano fijando x.

    Recibe:
      cubo de juego
      coordenada x del plano
    Devuelve:
      representación del plano
    Excepciones:
        Ninguna"""

    dibujo = f"========= PLANO x = {x} =========\n"

    dibujo += "    "
    for z in range(len(cubo)):
        dibujo += f"z{z + 1} "
    dibujo += "\n"

    for y in range(len(cubo[0])):
        dibujo += f"y{y + 1}  "
        for z in range(len(cubo)):
            dibujo += f"{cubo[z][y][x - 1]}  "
        dibujo += "\n"

    return dibujo


def dibujar_plano_y(cubo, y):
    """Dibuja un plano fijando y.

    Recibe:
       cubo
       coordenada y del plano
    Devuelve:
        representación del plano
      Excepciones:
        Ninguna"""
    dibujo = f"========= PLANO y = {y} =========\n"

    dibujo += "    "
    for x in range(len(cubo[0][y - 1])):
        dibujo += f"x{x + 1} "
    dibujo += "\n"

    for z in range(len(cubo)):
        dibujo += f"z{z + 1}  "
        for x in range(len(cubo[z][y - 1])):
            dibujo += f"{cubo[z][y - 1][x]}  "
        dibujo += "\n"

    return dibujo
def obtener_vecinos(cubo, punto):
    """Obtiene los vecinos directos
    Recibe:
        cubo
        punto

    Devuelve:
        lista de coordenadas vecinas válidas

    Excepciones:
        Ninguna
    """
    z, x, y = punto
    vecinos = []
    n = len(cubo)

    puntos = [
        (z - 1, x, y),
        (z + 1, x, y),
        (z, x - 1, y),
        (z, x + 1, y),
        (z, x, y - 1),
        (z, x, y + 1)
    ]

    for p in puntos:
        if punto_valido(p, n):
            vecinos.append(p)

    return vecinos


def recorrer_por_capas(cubo):
    """Recorre el cubo por capas de z.

    Recibe:
        cubo (list): cubo de juego.

    Devuelve:
        list: puntos recorridos en orden (z, x, y).

     Excepciones:
        Ninguna"""

    recorrido = []
    n = len(cubo)

    for z in range(1, n + 1):
        for y in range(1, n + 1):
            for x in range(1, n + 1):
                punto = (z, x, y)
                recorrido.append(punto)

    return recorrido
