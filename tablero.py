"""
Clase encargada de crear y manipular el tablero tridimensional.

Los puntos se representan mediante coordenadas (z, x, y),
con valores desde 1 hasta N.

El cubo se almacena internamente como:
cubo[z - 1][y - 1][x - 1].
"""


# Estados de las celdas
AGUA_SIN_EXPLORAR = "~"
NAVE_OCULTA = "?"
AGUA_MARCADA = "A"
IMPACTO = "X"
HUNDIDO = "#"
DETECTADO_SONAR = "D"


# Excepciones propias
class ErrorTablero(Exception):
    """Error general del tablero."""


class PuntoInvalidoError(ErrorTablero):
    """Se lanza cuando un punto no pertenece al cubo."""


class DimensionesError(ErrorTablero):
    """Se lanza cuando las dimensiones de matrices no son compatibles."""


def crear_cubo(n=8):
    """Crea un cubo vacío de N×N×N celdas

    Recibe:
     tamaño del cubo.

    Devuelve:
       cubo como lista de listas de listas, celdas inicializadas con "~"

    Excepciones:
            ErrorTablero: si el tamaño es menor que 1."""

    if n < 1:
        raise ErrorTablero("El tamaño debe ser un entero mayor o igual a 1.")

    cubo = []
    for z in range(n):
        capa = []
        for y in range(n):
            fila = []
            for x in range(n):
                fila.append(AGUA_SIN_EXPLORAR)
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
            PuntoInvalidoError: si la coordenada no pertenece al cubo."""

    if z < 1 or z > len(cubo):
        raise PuntoInvalidoError("La capa Z no pertenece al cubo.")

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
        DimensionesError: si las matrices tienen distinto tamaño."""
    if len(a) != len(b):
        raise DimensionesError("Las matrices deben tener el mismo tamaño.")

    for i in range(len(a)):
        if len(a[i]) != len(b[i]):
            raise DimensionesError("Las matrices deben tener el mismo tamaño.")

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
        DimensionesError: si las matrices tienen distinto tamaño."""

    if len(a) != len(b):
        raise DimensionesError("Las matrices deben tener el mismo tamaño.")

    for i in range(len(a)):
        if len(a[i]) != len(b[i]):
            raise DimensionesError("Las matrices deben tener el mismo tamaño.")

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
       DimensionesError: si las matrices están vacías o no son compatibles."""

    if len(a) == 0 or len(b) == 0:
        raise DimensionesError("Las matrices no pueden estar vacías.")

    filas_a = len(a)
    columnas_a = len(a[0])
    columnas_b = len(b[0])
    resultado = []
    if columnas_a != len(b):
        raise DimensionesError("Las matrices no tienen dimensiones compatibles.")

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
        DimensionesError: si la matriz está vacía.
    """

    if len(matriz) == 0:
        raise DimensionesError("La matriz no puede estar vacía.")

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
      PuntoInvalidoError: si la coordenada no pertenece al cubo."""

    if x < 1 or x > len(cubo[0][0]):
        raise PuntoInvalidoError("El plano X no pertenece al cubo.")

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
        PuntoInvalidoError: si la coordenada no pertenece al cubo."""

    if y < 1 or y > len(cubo[0]):
        raise PuntoInvalidoError("El plano Y no pertenece al cubo.")

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
        PuntoInvalidoError: si el punto no pertenece al cubo.
    """
    n = len(cubo)

    if not punto_valido(punto, n):
        raise PuntoInvalidoError("El punto no pertenece al cubo.")

    z, x, y = punto
    vecinos = []

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

def recorrer_por_columnas(cubo):
    """
    Recorre el cubo por columnas.

    Recibe:
        cubo: cubo tridimensional.

    Devuelve:
        Una lista de puntos ordenados por columna.
    """
    recorrido = []
    n = len(cubo)

    for x in range(1, n + 1):
        for z in range(1, n + 1):
            for y in range(1, n + 1):
                recorrido.append((z, x, y))

    return recorrido

def recorrer_por_filas(cubo):
    """
    Recorre el cubo comenzando por las filas.

    Recibe:
        cubo: cubo tridimensional.

    Devuelve:
        list: puntos recorridos en orden (z, x, y).
    """
    recorrido = []
    n = len(cubo)

    for y in range(1, n + 1):
        for z in range(1, n + 1):
            for x in range(1, n + 1):
                recorrido.append((z, x, y))

    return recorrido

def distancia_entre_puntos(punto1, punto2):
    distancia = 0
    for coordenada in (punto1 - punto2):
        distancia += abs(coordenada)

    return distancia


def son_puntos_en_linea_recta(punto1, punto2):
    if len(punto1) != len(punto2): return false
    variacion_de_coordenada = 0
    for coordenada in (0, len(punto1)):
        if punto1[coordenada] != punto2[coordenada]: ++variacion_de_coordenada
    return variacion_de_coordenada < 2
