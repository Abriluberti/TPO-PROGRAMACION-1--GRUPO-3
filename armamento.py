"""
Funciones para calcular las celdas afectadas por las armas
y administrar la munición del juego Operación Cubo.
"""


def _validar_punto(punto, n):
    """Valida un punto con coordenadas (z, x, y).

    Recibe:
        punto: tupla con las tres coordenadas.
        n: tamaño del cubo.

    Devuelve:
        True si las coordenadas están entre 1 y n; False en caso contrario.

    Excepciones:
        No lanza excepciones intencionalmente.
    """
    if len(punto) != 3:
        return False

    for valor in punto:
        if valor < 1 or valor > n:
            return False

    return True


def torpedo(cubo, punto, eje=None):
    """Calcula la celda afectada por un torpedo.

    Recibe:
        cubo: cubo de juego.
        punto: coordenadas (z, x, y).
        eje: parámetro opcional que no se utiliza.

    Devuelve:
        Un conjunto con el punto indicado, o un conjunto vacío
        si el punto no es válido.

    Excepciones:
        No lanza excepciones intencionalmente.
    """
    if not _validar_punto(punto, len(cubo)):
        return set()

    celdas = set()
    celdas.add(punto)

    return celdas


def racimo(cubo, punto, eje=None):
    """Calcula las celdas afectadas por un misil de racimo.

    Recibe:
        cubo: cubo de juego.
        punto: coordenadas (z, x, y).
        eje: parámetro opcional que no se utiliza.

    Devuelve:
        Un conjunto con el punto indicado y sus seis vecinos
        ortogonales que estén dentro del cubo. Si el punto no
        es válido, devuelve un conjunto vacío.

    Excepciones:
        No lanza excepciones intencionalmente.
    """
    n = len(cubo)

    if not _validar_punto(punto, n):
        return set()

    z, x, y = punto
    celdas = set()
    celdas.add(punto)

    vecinos = (
        (z + 1, x, y),
        (z - 1, x, y),
        (z, x + 1, y),
        (z, x - 1, y),
        (z, x, y + 1),
        (z, x, y - 1)
    )

    for vecino in vecinos:
        if _validar_punto(vecino, n):
            celdas.add(vecino)

    return celdas


def carga_profundidad(cubo, punto, eje=None):
    """Calcula las celdas de la recta del eje z.

    Recibe:
        cubo: cubo de juego.
        punto: coordenadas (z, x, y).
        eje: parámetro opcional que no se utiliza.

    Devuelve:
        Un conjunto con todas las celdas que comparten las
        coordenadas x e y del punto. Si el punto no es válido,
        devuelve un conjunto vacío.

    Excepciones:
        No lanza excepciones intencionalmente.
    """
    n = len(cubo)

    if not _validar_punto(punto, n):
        return set()

    z, x, y = punto
    celdas = set()

    for z in range(1, n + 1):
        celdas.add((z, x, y))

    return celdas


def barrido_laser(cubo, punto, eje=None):
    """Calcula las celdas de una recta sobre el eje x o y.

    Recibe:
        cubo: cubo de juego.
        punto: coordenadas (z, x, y).
        eje: eje de recorrido, 'x' o 'y'.

    Devuelve:
        Un conjunto con todas las celdas de la recta elegida.
        Si el punto o el eje no son válidos, devuelve un
        conjunto vacío.

    Excepciones:
        No lanza excepciones intencionalmente.
    """
    n = len(cubo)

    if not _validar_punto(punto, n):
        return set()

    z, x, y = punto
    celdas = set()

    if eje == "x":
        for x in range(1, n + 1):
            celdas.add((z, x, y))
    elif eje == "y":
        for y in range(1, n + 1):
            celdas.add((z, x, y))
    else:
        return set()

    return celdas


CATALOGO = {
    "T": None,
    "R": 3,
    "C": 2,
    "S": 4,
    "L": 2,
    "O": 1,
    "G": 1
}


ARMAS = {
    "T": torpedo,
    "R": racimo,
    "C": carga_profundidad,
    "L": barrido_laser
}


def municion_inicial():
    """Crea el inventario inicial de munición.

    Recibe:
        Ningún parámetro.

    Devuelve:
        Un diccionario con la munición inicial de cada arma.
        None representa munición ilimitada.

    Excepciones:
        No lanza excepciones intencionalmente.
    """
    municion = {}

    for letra in CATALOGO:
        municion[letra] = CATALOGO[letra]

    return municion


def tiene_municion(letra, municion):
    """Comprueba si queda munición para un arma.

    Recibe:
        letra: letra que identifica el arma.
        municion: diccionario con las cantidades disponibles.

    Devuelve:
        True si el arma tiene munición disponible o ilimitada;
        False si la letra no existe o la munición se agotó.

    Excepciones:
        No lanza excepciones intencionalmente.
    """
    if letra not in municion:
        return False

    if municion[letra] is None:
        return True

    return municion[letra] > 0


def gastar_municion(letra, municion):
    """Descuenta una unidad de munición cuando corresponde.

    Recibe:
        letra: letra que identifica el arma.
        municion: diccionario con las cantidades disponibles.

    Devuelve:
        El mismo diccionario, actualizado si había munición
        finita disponible. La munición ilimitada no se descuenta.

    Excepciones:
        No lanza excepciones intencionalmente.
    """
    if tiene_municion(letra, municion):
        if municion[letra] is not None:
            municion[letra] = municion[letra] - 1

    return municion


def disparar(letra, cubo, punto, eje=None):
    """Calcula las celdas afectadas por el arma seleccionada.

    Recibe:
        letra: letra que identifica el arma.
        cubo: cubo de juego.
        punto: coordenadas (z, x, y).
        eje: eje opcional para el barrido láser.

    Devuelve:
        El conjunto de celdas afectadas. Si el arma no está
        implementada en este módulo o el punto no es válido,
        devuelve un conjunto vacío.

    Excepciones:
        No lanza excepciones intencionalmente.
    """
    funcion = ARMAS.get(letra)

    if funcion is None:
        return set()

    return funcion(cubo, punto, eje)


def aplicar_disparo(letra, cubo, punto, ocupadas, municion, eje=None):
    """Calcula los impactos y el agua de un disparo válido.

    Recibe:
        letra: letra que identifica el arma.
        cubo: cubo de juego.
        punto: coordenadas (z, x, y).
        ocupadas: conjunto de celdas ocupadas por naves.
        municion: diccionario con la munición disponible.
        eje: eje opcional para el barrido láser.

    Devuelve:
        Un diccionario con los conjuntos 'celdas', 'impactos'
        y 'agua'. Si el disparo es inválido o no hay munición,
        los tres conjuntos están vacíos.

    Excepciones:
        No lanza excepciones intencionalmente.
    """
    vacio = {
        "celdas": set(),
        "impactos": set(),
        "agua": set()
    }

    if not tiene_municion(letra, municion):
        return vacio

    celdas = disparar(letra, cubo, punto, eje)

    if not celdas:
        return vacio

    impactos = celdas & ocupadas
    agua = celdas - impactos

    gastar_municion(letra, municion)

    return {
        "celdas": celdas,
        "impactos": impactos,
        "agua": agua
    }
