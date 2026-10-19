def _validar_punto(punto, n):
    if len(punto) != 3:
        return False

    for valor in punto:
        if valor < 1 or valor > n:
            return False

    return True


def torpedo(cubo, punto, eje=None):
    if not _validar_punto(punto, len(cubo)):
        return set()

    celdas = set()
    celdas.add(punto)

    return celdas


def racimo(cubo, punto, eje=None):
    n = len(cubo)

    if not _validar_punto(punto, n):
        return set()

    z, x, y = punto
    celdas = set()
    celdas.add(punto)

    direcciones = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1)
    ]

    for direccion in direcciones:
        dz, dx, dy = direccion

        nz = z + dz
        nx = x + dx
        ny = y + dy

        if 1 <= nz <= n and 1 <= nx <= n and 1 <= ny <= n:
            celdas.add((nz, nx, ny))

    return celdas


def carga_profundidad(cubo, punto, eje=None):
    n = len(cubo)

    if not _validar_punto(punto, n):
        return set()

    z, x, y = punto
    celdas = set()

    for i in range(1, n + 1):
        celdas.add((i, x, y))

    return celdas


def barrido_laser(cubo, punto, eje=None):
    n = len(cubo)

    if not _validar_punto(punto, n):
        return set()

    if eje != "x" and eje != "y":
        return set()

    z, x, y = punto
    celdas = set()

    for i in range(1, n + 1):
        if eje == "x":
            celdas.add((z, i, y))
        else:
            celdas.add((z, x, i))

    return celdas


CATALOGO = {
    "T": {
        "nombre": "torpedo",
        "municion": None,
        "funcion": torpedo
    },
    "R": {
        "nombre": "misil de racimo",
        "municion": 3,
        "funcion": racimo
    },
    "C": {
        "nombre": "carga de profundidad",
        "municion": 2,
        "funcion": carga_profundidad
    },
    "S": {
        "nombre": "sonar",
        "municion": 4
    },
    "L": {
        "nombre": "barrido laser",
        "municion": 2,
        "funcion": barrido_laser
    },
    "O": {
        "nombre": "onda expansiva",
        "municion": 1
    },
    "G": {
        "nombre": "torpedo guiado",
        "municion": 1
    }
}


def municion_inicial():
    municion = {}

    for letra in CATALOGO:
        municion[letra] = CATALOGO[letra]["municion"]

    return municion


def tiene_municion(municion, letra):
    if letra not in municion:
        return False

    cantidad = municion[letra]

    if cantidad is None:
        return True

    if cantidad > 0:
        return True

    return False


def gastar_municion(municion, letra):
    if not tiene_municion(municion, letra):
        return municion

    if municion[letra] is not None:
        municion[letra] = municion[letra] - 1

    return municion


def disparar(letra, cubo, punto, eje=None):
    if letra not in CATALOGO:
        return set()

    if "funcion" not in CATALOGO[letra]:
        return set()

    funcion = CATALOGO[letra]["funcion"]

    return funcion(cubo, punto, eje)


def aplicar_disparo(letra, cubo, punto, ocupadas, municion, eje=None):
    if not tiene_municion(municion, letra):
        return {
            "celdas": set(),
            "impactos": set(),
            "agua": set()
        }

    celdas = disparar(letra, cubo, punto, eje)

    if len(celdas) == 0:
        return {
            "celdas": set(),
            "impactos": set(),
            "agua": set()
        }

    impactos = celdas & ocupadas
    agua = celdas - impactos

    gastar_municion(municion, letra)

    resultado = {
        "celdas": celdas,
        "impactos": impactos,
        "agua": agua
    }

    return resultado