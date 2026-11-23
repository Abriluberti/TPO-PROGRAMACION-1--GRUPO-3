"""Armas, celdas afectadas y administración de munición de Operación Cubo."""


def _validar_punto(punto, n):
    """Valida una coordenada (z, x, y) dentro del cubo."""
    if not isinstance(punto, (tuple, list)) or len(punto) != 3:
        return False

    for valor in punto:
        if not isinstance(valor, int) or isinstance(valor, bool):
            return False

        if valor < 1 or valor > n:
            return False

    return True


def _vecinos(punto):
    """Devuelve los seis vecinos ortogonales de una celda."""
    z, x, y = punto
    return (
        (z + 1, x, y), (z - 1, x, y),
        (z, x + 1, y), (z, x - 1, y),
        (z, x, y + 1), (z, x, y - 1)
    )


def torpedo(cubo, punto, eje=None, flota=None):
    """Devuelve solamente la celda apuntada."""
    if not _validar_punto(punto, len(cubo)):
        return set()
    return {tuple(punto)}


def racimo(cubo, punto, eje=None, flota=None):
    """Devuelve el punto apuntado y sus seis vecinos válidos."""
    n = len(cubo)
    if not _validar_punto(punto, n):
        return set()

    punto = tuple(punto)
    celdas = {punto}

    for vecino in _vecinos(punto):
        if _validar_punto(vecino, n):
            celdas.add(vecino)

    return celdas


def carga_profundidad(cubo, punto, eje=None, flota=None):
    """Devuelve la recta completa del eje z que pasa por el punto."""
    n = len(cubo)
    if not _validar_punto(punto, n):
        return set()

    z, x, y = punto
    celdas = set()

    for coordenada_z in range(1, n + 1):
        celdas.add((coordenada_z, x, y))

    return celdas


def barrido_laser(cubo, punto, eje=None, flota=None):
    """Devuelve una recta completa sobre x o sobre y."""
    n = len(cubo)
    if not _validar_punto(punto, n):
        return set()

    z, x, y = punto
    celdas = set()

    if eje == "x":
        for coordenada_x in range(1, n + 1):
            celdas.add((z, coordenada_x, y))
    elif eje == "y":
        for coordenada_y in range(1, n + 1):
            celdas.add((z, x, coordenada_y))
    else:
        return set()

    return celdas


# La consigna pide radio decreciente, pero no fija el radio inicial.
# Se adopta 2 como criterio inicial del grupo y queda centralizado aquí.
RADIO_ONDA = 2


def _propagar_onda(cubo, frontera, radio, visitadas):
    """Expande una frontera de celdas y continúa con radio decreciente."""
    if radio < 0 or not frontera:
        return visitadas

    for punto in frontera:
        visitadas.add(punto)

    if radio == 0:
        return visitadas

    nueva_frontera = set()

    for punto in frontera:
        for vecino in _vecinos(punto):
            if _validar_punto(vecino, len(cubo)):
                if vecino not in visitadas:
                    nueva_frontera.add(vecino)

    return _propagar_onda(
        cubo, nueva_frontera, radio - 1, visitadas
    )


def onda_expansiva(cubo, punto, eje=None, flota=None, radio=RADIO_ONDA):
    """Calcula recursivamente las celdas alcanzadas por la onda expansiva."""
    if not _validar_punto(punto, len(cubo)):
        return set()

    if not isinstance(radio, int) or isinstance(radio, bool) or radio < 0:
        return set()

    return _propagar_onda(
        cubo, {tuple(punto)}, radio, set()
    )


def _buscar_celda_contigua(nave, punto, visitadas):
    """Busca recursivamente una celda no impactada de la misma nave."""
    celdas_nave = {tuple(celda) for celda in nave.get("celdas", [])}
    impactos = {tuple(celda) for celda in nave.get("impactos", set())}

    if punto in visitadas:
        return None

    visitadas.add(punto)

    for vecino in _vecinos(punto):
        if vecino in celdas_nave:
            if vecino not in impactos:
                return vecino

            encontrada = _buscar_celda_contigua(
                nave, vecino, visitadas
            )
            if encontrada is not None:
                return encontrada

    return None


def torpedo_guiado(cubo, punto, eje=None, flota=None):
    """Busca una celda contigua a un impacto previo de una nave no hundida."""
    if flota is None or not _validar_punto(punto, len(cubo)):
        return set()

    punto = tuple(punto)

    for nave in flota:
        if nave.get("hundida", False):
            continue

        impactos = {
            tuple(celda) for celda in nave.get("impactos", set())
        }

        if punto in impactos:
            encontrada = _buscar_celda_contigua(
                nave, punto, set()
            )
            if encontrada is not None:
                return {encontrada}

    return set()


CATALOGO = {
    "T": None,
    "R": 3,
    "C": 2,
    "S": 4,
    "L": 2,
    "O": 1,
    "G": 1
}


# El sonar S se procesa en radar.py porque no produce daño.
ARMAS = {
    "T": torpedo,
    "R": racimo,
    "C": carga_profundidad,
    "L": barrido_laser,
    "O": onda_expansiva,
    "G": torpedo_guiado
}


def municion_inicial():
    """Devuelve un diccionario con la munición inicial de todas las armas."""
    municion = {}
    for letra in CATALOGO:
        municion[letra] = CATALOGO[letra]
    return municion


def tiene_municion(letra, municion):
    """Indica si existe munición disponible o ilimitada para el arma."""
    if letra not in municion:
        return False
    if municion[letra] is None:
        return True
    return municion[letra] > 0


def gastar_municion(letra, municion):
    """Descuenta una unidad de munición finita y devuelve el inventario."""
    if tiene_municion(letra, municion):
        if municion[letra] is not None:
            municion[letra] -= 1
    return municion


def disparar(letra, cubo, punto, eje=None, flota=None):
    """Despacha el arma y devuelve las celdas afectadas."""
    if letra not in ARMAS:
        return set()
    if not _validar_punto(punto, len(cubo)):
        return set()

    funcion = ARMAS[letra]
    return funcion(cubo, punto, eje, flota)


def aplicar_disparo(letra, cubo, punto, ocupadas, municion,
                    eje=None, flota=None, disparos_previos=None):
    """Devuelve celdas, impactos y agua; descuenta munición si dispara."""
    vacio = {
        "celdas": set(),
        "impactos": set(),
        "agua": set()
    }

    if not tiene_municion(letra, municion):
        return vacio

    celdas = disparar(letra, cubo, punto, eje, flota)

    if disparos_previos is not None:
        celdas = celdas - disparos_previos

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


