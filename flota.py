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

    if reglas == "submarino":
        for z, x, y in celdas:
            if z > mitad:
                raise FlotaError("El submarino solo puede ubicarse en la mitad inferior de z.")

    if reglas == "crucero":
        for z, x, y in celdas:
            if z == 1 or z == n:
                raise FlotaError("El crucero no puede ocupar z = 1 ni z = N.")

    if reglas == "portaaviones":
        for z, x, y in celdas:
            if z <= mitad:
                raise FlotaError("El portaaviones solo puede ubicarse en la mitad superior de z.")

    if reglas == "estacion":
        for z, x, y in celdas:
            if z == 1 or z == n or x == 1 or x == n or y == 1 or y == n:
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


def contar_ubicadas(flota, letra):
    """Cuenta cuantas naves de una letra ya estan en la flota.

    Recibe:
        flota: lista de naves ya ubicadas.
        letra: letra de la nave a contar.

    Devuelve:
        La cantidad de naves con esa letra que ya tiene la flota.
    """
    cantidad = 0
    for nave in flota:
        if nave["letra"] == letra:
            cantidad += 1
    return cantidad


def total_naves(catalogo):
    """Cantidad total de naves que tiene que tener una flota completa.

    Recibe:
        catalogo: catalogo de naves (ver CATALOGO_NAVES).

    Devuelve:
        La suma de las cantidades de cada tipo de nave del catalogo.
    """
    total = 0
    for datos_nave in catalogo.values():
        total += datos_nave["cantidad"]
    return total


def cantidad_pendiente(flota, catalogo, letra):
    """Cuantas naves de una letra faltan ubicar todavia.

    Recibe:
        flota: lista de naves ya ubicadas.
        catalogo: catalogo de naves.
        letra: letra de la nave.

    Devuelve:
        La cantidad que falta ubicar de esa letra (0 si ya estan todas).
    """
    return catalogo[letra]["cantidad"] - contar_ubicadas(flota, letra)


def letras_pendientes(flota, catalogo):
    """Letras de naves a las que todavia les falta alguna por ubicar.

    Recibe:
        flota: lista de naves ya ubicadas.
        catalogo: catalogo de naves.

    Devuelve:
        Lista de letras con cantidad pendiente mayor a 0, en el mismo
        orden en que aparecen en el catalogo.
    """
    pendientes = []
    for letra in catalogo:
        if cantidad_pendiente(flota, catalogo, letra) > 0:
            pendientes.append(letra)
    return pendientes


def flota_completa(flota, catalogo):
    """Indica si ya se ubicaron todas las naves del catalogo.

    Recibe:
        flota: lista de naves ya ubicadas.
        catalogo: catalogo de naves.

    Devuelve:
        True si la flota ya tiene todas las naves del catalogo.
    """
    return len(flota) >= total_naves(catalogo)


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
        "impactos_parciales", "hundida"}.

    Lanza:
        FlotaError si la letra no existe, si ya se ubicaron todas las
        naves de ese tipo, o si el tramo no cumple alguna regla de
        ubicacion (tamanio, alineacion, bordes o separacion).
    """
    if letra not in CATALOGO_NAVES:
        raise FlotaError("Nave invalida: debe ser F, D, S, C, P o E.")

    datos_nave = CATALOGO_NAVES[letra]
    ya_ubicadas = contar_ubicadas(flota, letra)

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
        # solo la usa el Portaaviones (cada celda necesita dos impactos),
        # pero se deja vacia en todas las naves para que el diccionario
        # tenga siempre la misma forma
        "impactos_parciales": set(),
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


def _ubicar_automatica_una_nave(cubo, flota, generador, letra, datos_nave, n):
    """Intenta ubicar una nave de un tipo en un tramo al azar, reintentando.

    Recibe:
        cubo, flota: estado actual.
        generador: random.Random ya inicializado (con o sin semilla).
        letra: letra de la nave a ubicar.
        datos_nave: entrada del catalogo para esa letra.
        n: tamanio del cubo.

    Devuelve:
        (cubo, flota) con la nueva nave agregada.

    Lanza:
        FlotaError si no se encuentra un lugar valido en INTENTOS_MAXIMOS
        intentos (el cubo esta demasiado lleno o es muy chico).
    """
    for _ in range(INTENTOS_MAXIMOS):
        punto_desde, punto_hasta = _tramo_aleatorio(generador, letra, datos_nave, n)

        try:
            return ubicar_nave(cubo, flota, letra, punto_desde, punto_hasta)
        except FlotaError:
            continue

    raise FlotaError(f"No se encontro lugar para la nave {datos_nave['nombre']}.")


def ubicacion_automatica(cubo, catalogo, semilla=None):
    """Ubica toda la flota de forma aleatoria, respetando las reglas.

    Recibe:
        cubo: cubo de juego.
        catalogo: catalogo de naves (ver CATALOGO_NAVES).
        semilla: semilla del generador aleatorio, para que la ubicacion
            sea reproducible. None usa aleatoriedad real.

    Devuelve:
        La flota ubicada (lista de naves). El cubo se modifica en el
        lugar (misma lista que se recibió), no hace falta reasignarlo.

    Lanza:
        FlotaError si, tras varios intentos, no se encuentra lugar
        para alguna nave (el cubo es demasiado chico para la flota).
    """
    generador = random.Random(semilla)
    n = len(cubo)
    flota = []

    # Se ubican primero las naves mas grandes y restringidas, y las mas
    # chicas al final: si se ubican en el orden del catalogo (Fragata
    # primero), para cuando le toca a la Estacion ya no queda lugar
    # facil y el sorteo al azar fallaba seguido (hasta 1 de cada 10
    # veces en un cubo de 8).

    # Estacion orbital (1 bloque de 2x2x2, no toca ninguna cara del cubo)
    datos_estacion = catalogo["E"]
    for _ in range(datos_estacion["cantidad"]):
        cubo, flota = _ubicar_automatica_una_nave(
            cubo, flota, generador, "E", datos_estacion, n
        )

    # Portaaviones (1 nave de 5 celdas, solo en la mitad superior de z)
    datos_portaaviones = catalogo["P"]
    for _ in range(datos_portaaviones["cantidad"]):
        cubo, flota = _ubicar_automatica_una_nave(
            cubo, flota, generador, "P", datos_portaaviones, n
        )

    # Crucero (1 nave de 4 celdas, no puede ocupar z = 1 ni z = N)
    datos_crucero = catalogo["C"]
    for _ in range(datos_crucero["cantidad"]):
        cubo, flota = _ubicar_automatica_una_nave(
            cubo, flota, generador, "C", datos_crucero, n
        )

    # Destructor (2 naves de 3 celdas, sin restriccion)
    datos_destructor = catalogo["D"]
    for _ in range(datos_destructor["cantidad"]):
        cubo, flota = _ubicar_automatica_una_nave(
            cubo, flota, generador, "D", datos_destructor, n
        )

    # Submarino (2 naves de 3 celdas, solo en la mitad inferior de z)
    datos_submarino = catalogo["S"]
    for _ in range(datos_submarino["cantidad"]):
        cubo, flota = _ubicar_automatica_una_nave(
            cubo, flota, generador, "S", datos_submarino, n
        )

    # Fragata (3 naves de 2 celdas, sin restriccion)
    datos_fragata = catalogo["F"]
    for _ in range(datos_fragata["cantidad"]):
        cubo, flota = _ubicar_automatica_una_nave(
            cubo, flota, generador, "F", datos_fragata, n
        )

    return flota


# Comportamientos propios de cada nave y estado de combate (impactos,
# averias y hundimiento). Estas funciones no imprimen ni piden datos:
# el integrador (partida.py) llama a cada una y decide que mostrar
# segun lo que le devuelven.

def es_inmune(nave, arma):
    """Indica si una nave es inmune a un arma por su comportamiento propio.

    El submarino no es alcanzado por el barrido laser.

    Recibe: nave (diccionario), arma (letra del arma).
    Devuelve: True si ese arma no puede afectar a esa nave.
    """
    return nave["letra"] == "S" and arma == "L"


def registrar_impacto(nave, punto):
    """Registra un impacto en una celda de la nave y actualiza su estado.

    Comportamiento propio del Portaaviones: cada celda necesita dos
    impactos para confirmarse como un impacto real; el primero queda
    como parcial.

    Recibe:
        nave: diccionario de la nave impactada.
        punto: celda impactada (debe pertenecer a nave["celdas"]).

    Devuelve:
        Diccionario con:
        "confirmado": False si es el primer impacto a una celda de
            Portaaviones (todavia no cuenta como impacto real).
        "recien_confirmada": True si esta celda pasa a contar como
            impacto real recien en este llamado.
        "recien_hundida": True si este impacto hundio la nave recien
            en este llamado.
    """
    if nave["letra"] == "P" and punto not in nave["impactos"]:
        if punto not in nave["impactos_parciales"]:
            nave["impactos_parciales"].add(punto)
            return {
                "confirmado": False,
                "recien_confirmada": False,
                "recien_hundida": False
            }

        nave["impactos_parciales"].remove(punto)

    recien_confirmada = punto not in nave["impactos"]
    nave["impactos"].add(punto)

    recien_hundida = False
    if not nave["hundida"] and nave["impactos"] == nave["celdas"]:
        nave["hundida"] = True
        recien_hundida = True

    return {
        "confirmado": True,
        "recien_confirmada": recien_confirmada,
        "recien_hundida": recien_hundida
    }


def impacto_pendiente(flota, punto):
    """Indica si una celda ya tiene un primer impacto y espera el segundo.

    Comportamiento propio del Portaaviones: mientras falte el segundo
    impacto para confirmar una celda, hay que poder volver a dispararle
    a esa misma celda.

    Recibe: flota (lista de naves), punto.
    Devuelve: True si hay que permitir disparar de nuevo a esa celda.
    """
    for nave in flota:
        if punto in nave["impactos_parciales"]:
            return True
    return False


def proximo_impacto_pendiente(flota):
    """Busca una celda con un primer impacto que espera el segundo.

    Recibe: flota (lista de naves).
    Devuelve: una celda (tupla) pendiente de confirmar, o None si no hay.
    """
    for nave in flota:
        if nave["impactos_parciales"]:
            return next(iter(nave["impactos_parciales"]))
    return None


def celdas_para_torpedo_guiado(flota):
    """Celdas ya impactadas de naves no hundidas.

    Son las celdas candidatas para el torpedo guiado, que busca desde
    ahi una celda vecina de la misma nave que todavia no fue impactada.

    Recibe: flota (lista de naves).
    Devuelve: set de celdas.
    """
    celdas = set()
    for nave in flota:
        if nave["impactos"] and not nave["hundida"]:
            celdas |= nave["impactos"]
    return celdas


def revela_celda_al_impactar(nave):
    """Indica si esta nave revela una celda del rival al ser impactada.

    Comportamiento propio del Destructor.

    Recibe: nave (diccionario).
    Devuelve: True si esta nave tiene ese comportamiento.
    """
    return nave["letra"] == "D"


def elegir_celda_sin_revelar(flota):
    """Elige al azar una celda ocupada de la flota que no fue impactada.

    Se usa para el comportamiento propio del Destructor (revelar una
    celda ocupada del rival al ser impactado).

    Recibe: flota (lista de naves).
    Devuelve: una celda (tupla), o None si no queda ninguna sin revelar.
    """
    celdas_sin_revelar = set()
    for nave in flota:
        celdas_sin_revelar |= (nave["celdas"] - nave["impactos"])

    if not celdas_sin_revelar:
        return None

    return random.choice(sorted(celdas_sin_revelar))


def otorga_municion_extra_al_hundirse(nave):
    """Indica si esta nave otorga municion extra al jugador al hundirse.

    Comportamiento propio de la Estacion orbital.

    Recibe: nave (diccionario).
    Devuelve: True si esta nave tiene ese comportamiento.
    """
    return nave["letra"] == "E"


def marcar_hundida(cubo, nave):
    """Marca en el cubo las celdas de una nave recien hundida.

    Recibe: cubo, nave (diccionario, ya con nave["hundida"] = True).
    Devuelve: None.
    """
    for z, x, y in nave["celdas"]:
        cubo[z - 1][y - 1][x - 1] = tablero.HUNDIDO


def toda_hundida(flota):
    """Indica si todas las naves de una flota estan hundidas.

    Recibe: flota (lista de naves).
    Devuelve: True si la flota no esta vacia y todas sus naves estan
        hundidas; False si esta vacia o le queda alguna a flote.
    """
    if not flota:
        return False

    for nave in flota:
        if not nave["hundida"]:
            return False

    return True
