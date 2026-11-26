"""Catalogo de naves y ubicacion de la flota en el cubo.

Este modulo no imprime ni pide datos por consola: recibe los puntos ya
elegidos (por un jugador o por el azar) y devuelve el cubo y la flota
actualizados, o lanza FlotaError si la ubicacion no es valida. El
integrador (partida.py) es el que arma el dialogo con el usuario.
"""
import random

import tablero


class FlotaError(Exception):
    """Error al ubicar una nave."""


# Catalogo de naves: tamanio (celdas que ocupa en linea recta, salvo la
# estacion que es un bloque 2x2x2), cantidad de naves de ese tipo por
# flota, y la restriccion de ubicacion propia (None = sin restriccion).
CATALOGO_NAVES = {
    "F": {"nombre": "Fragata", "tamanio": 2, "cantidad": 3, "reglas": None},
    "D": {"nombre": "Destructor", "tamanio": 3, "cantidad": 2, "reglas": None},
    "S": {"nombre": "Submarino", "tamanio": 3, "cantidad": 2, "reglas": "submarino"},
    "C": {"nombre": "Crucero", "tamanio": 4, "cantidad": 1, "reglas": "crucero"},
    "P": {"nombre": "Portaaviones", "tamanio": 5, "cantidad": 1, "reglas": "portaaviones"},
    "E": {"nombre": "Estacion", "tamanio": 8, "cantidad": 1, "reglas": "estacion"},
}

# tope de intentos al azar por nave antes de rendirse (evita loop infinito
# cuando el cubo es demasiado chico para la flota completa)
INTENTOS_MAXIMOS = 400


def _celdas_del_tramo(punto_desde, punto_hasta):
    """Calcula las celdas de una nave recta entre dos puntos extremos.

    Recibe:
        punto_desde, punto_hasta: tuplas (z, x, y).

    Devuelve:
        Lista de tuplas (z, x, y), del extremo "desde" al "hasta".

    Lanza:
        FlotaError si los puntos no estan alineados en un solo eje.
    """
    z1, x1, y1 = punto_desde
    z2, x2, y2 = punto_hasta

    ejes_distintos = sum(1 for a, b in ((z1, z2), (x1, x2), (y1, y2)) if a != b)
    if ejes_distintos > 1:
        raise FlotaError("Las celdas de la nave deben estar en linea recta.")

    if z1 != z2:
        paso = 1 if z2 > z1 else -1
        return [(z, x1, y1) for z in range(z1, z2 + paso, paso)]

    if x1 != x2:
        paso = 1 if x2 > x1 else -1
        return [(z1, x, y1) for x in range(x1, x2 + paso, paso)]

    if y1 != y2:
        paso = 1 if y2 > y1 else -1
        return [(z1, x1, y) for y in range(y1, y2 + paso, paso)]

    return [(z1, x1, y1)]


def _celdas_del_bloque(punto_desde, punto_hasta):
    """Calcula las 8 celdas del bloque 2x2x2 de la estacion orbital.

    Recibe:
        punto_desde, punto_hasta: dos esquinas opuestas del bloque.

    Devuelve:
        Lista de 8 tuplas (z, x, y).

    Lanza:
        FlotaError si los puntos no forman un bloque de 2x2x2.
    """
    z1, x1, y1 = punto_desde
    z2, x2, y2 = punto_hasta

    if abs(z1 - z2) != 1 or abs(x1 - x2) != 1 or abs(y1 - y2) != 1:
        raise FlotaError("La estacion debe ocupar un bloque de 2x2x2.")

    return [(z, x, y) for z in (z1, z2) for x in (x1, x2) for y in (y1, y2)]


def _validar_regla(letra, celdas, n):
    """Valida la restriccion de ubicacion propia del tipo de nave.

    Recibe:
        letra: letra de la nave.
        celdas: celdas que ocuparia.
        n: tamanio del cubo.

    Lanza:
        FlotaError si no cumple su restriccion.
    """
    reglas = CATALOGO_NAVES[letra]["reglas"]
    mitad = n / 2

    if reglas == "submarino" and any(z > mitad for z, x, y in celdas):
        raise FlotaError("El submarino solo puede ubicarse en la mitad inferior de z.")

    if reglas == "crucero" and any(z == 1 or z == n for z, x, y in celdas):
        raise FlotaError("El crucero no puede ocupar z = 1 ni z = N.")

    if reglas == "portaaviones" and any(z <= mitad for z, x, y in celdas):
        raise FlotaError("El portaaviones solo puede ubicarse en la mitad superior de z.")

    if reglas == "estacion" and any(
        z in (1, n) or x in (1, n) or y in (1, n) for z, x, y in celdas
    ):
        raise FlotaError("La estacion no puede tocar ninguna cara exterior del cubo.")


def _validar_lugar(cubo, celdas, n):
    """Valida que las celdas esten libres y separadas de otras naves.

    Entre dos naves debe quedar al menos una celda libre en cualquier
    direccion, incluidas las diagonales.

    Recibe:
        cubo, celdas (de la nave a ubicar), n (tamanio del cubo).

    Lanza:
        FlotaError si alguna celda esta fuera del cubo, ocupada, o
        pegada a otra nave.
    """
    celdas_nave = set(celdas)

    for z, x, y in celdas:
        if not tablero.punto_valido((z, x, y), n):
            raise FlotaError("La nave no puede salir del cubo.")

        if cubo[z - 1][y - 1][x - 1] != tablero.AGUA_SIN_EXPLORAR:
            raise FlotaError("Ya hay otra nave ocupando esa posicion.")

        for vz in (z - 1, z, z + 1):
            for vx in (x - 1, x, x + 1):
                for vy in (y - 1, y, y + 1):
                    vecino = (vz, vx, vy)
                    if vecino in celdas_nave:
                        continue
                    if tablero.punto_valido(vecino, n):
                        if cubo[vz - 1][vy - 1][vx - 1] != tablero.AGUA_SIN_EXPLORAR:
                            raise FlotaError(
                                "Debe quedar al menos una celda libre entre naves."
                            )


def ubicar_nave(cubo, flota, letra, punto_desde, punto_hasta):
    """Ubica una nave en el cubo segun su letra y el tramo que ocupa.

    Recibe:
        cubo: cubo de juego (lista de listas de listas).
        flota: lista de naves ya ubicadas (lista de diccionarios).
        letra: letra de la nave a ubicar (F, D, S, C, P o E).
        punto_desde, punto_hasta: extremos del tramo (z, x, y). Para la
            estacion orbital son dos esquinas opuestas del bloque 2x2x2.

    Devuelve:
        (cubo, flota) actualizados, con la nueva nave agregada a la
        flota como un diccionario {"letra", "celdas", "impactos",
        "hundida"}.

    Lanza:
        FlotaError si la letra no existe, si ya se ubicaron todas las
        naves de ese tipo, o si el tramo no cumple alguna regla de
        ubicacion (tamanio, alineacion, bordes o separacion).
    """
    if letra not in CATALOGO_NAVES:
        raise FlotaError("Nave invalida: debe ser F, D, S, C, P o E.")

    datos_nave = CATALOGO_NAVES[letra]
    ya_ubicadas = sum(1 for nave in flota if nave["letra"] == letra)

    if ya_ubicadas >= datos_nave["cantidad"]:
        raise FlotaError(f"Ya se ubicaron todas las naves {datos_nave['nombre']}.")

    n = len(cubo)

    if letra == "E":
        celdas = _celdas_del_bloque(punto_desde, punto_hasta)
    else:
        celdas = _celdas_del_tramo(punto_desde, punto_hasta)
        if len(celdas) != datos_nave["tamanio"]:
            raise FlotaError(f"La nave debe ocupar {datos_nave['tamanio']} celdas.")

    _validar_regla(letra, celdas, n)
    _validar_lugar(cubo, celdas, n)

    for z, x, y in celdas:
        cubo[z - 1][y - 1][x - 1] = tablero.NAVE_OCULTA

    nave = {
        "letra": letra,
        "celdas": set(celdas),
        "impactos": set(),
        "hundida": False
    }
    flota = flota + [nave]

    return cubo, flota


def _tramo_aleatorio(generador, letra, datos_nave, n):
    """Genera un tramo (o bloque) al azar para intentar ubicar una nave.

    No garantiza que el tramo sea valido: ubicacion_automatica reintenta
    las veces que haga falta si ubicar_nave lo rechaza.
    """
    if letra == "E":
        punto_desde = (
            generador.randint(1, n),
            generador.randint(1, n),
            generador.randint(1, n)
        )
        punto_hasta = tuple(
            coordenada + generador.choice((1, -1)) for coordenada in punto_desde
        )
        return punto_desde, punto_hasta

    tamanio = datos_nave["tamanio"]
    eje = generador.choice(("z", "x", "y"))
    sentido = generador.choice((1, -1))
    z, x, y = (
        generador.randint(1, n),
        generador.randint(1, n),
        generador.randint(1, n)
    )
    punto_desde = (z, x, y)

    if eje == "z":
        punto_hasta = (z + sentido * (tamanio - 1), x, y)
    elif eje == "x":
        punto_hasta = (z, x + sentido * (tamanio - 1), y)
    else:
        punto_hasta = (z, x, y + sentido * (tamanio - 1))

    return punto_desde, punto_hasta


def ubicacion_automatica(cubo, catalogo, semilla=None):
    """Ubica toda la flota de forma aleatoria, respetando las reglas.

    Recibe:
        cubo: cubo de juego.
        catalogo: catalogo de naves (ver CATALOGO_NAVES).
        semilla: semilla del generador aleatorio, para que la ubicacion
            sea reproducible. None usa aleatoriedad real.

    Devuelve:
        (cubo, flota) con todas las naves del catalogo ubicadas.

    Lanza:
        FlotaError si, tras varios intentos, no se encuentra lugar
        para alguna nave (el cubo es demasiado chico para la flota).
    """
    generador = random.Random(semilla)
    n = len(cubo)
    flota = []

    for letra, datos_nave in catalogo.items():
        for _ in range(datos_nave["cantidad"]):
            ubicada = False

            for _ in range(INTENTOS_MAXIMOS):
                punto_desde, punto_hasta = _tramo_aleatorio(
                    generador, letra, datos_nave, n
                )
                try:
                    cubo, flota = ubicar_nave(
                        cubo, flota, letra, punto_desde, punto_hasta
                    )
                    ubicada = True
                    break
                except FlotaError:
                    continue

            if not ubicada:
                raise FlotaError(
                    f"No se encontro lugar para la nave {datos_nave['nombre']}."
                )

    return cubo, flota
