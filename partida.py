
import re
import random
import armamento
import tablero
import flota



PATRON_MENU_TURNO = r"^[1-3]$"
PATRON_ARMA = r"^[TRCL]$"
PATRON_OBJETIVO = r"^(\d+),(\d+),(\d+)$"
PATRON_EJE = r"^[zxy]$"


def pedir_arma():
    """
    Pide y valida el arma seleccionada.
    Devuelve la letra del arma elegida.
    """

    while True:
        arma = input("Arma (T/R/C/L): ").strip().upper()

        if arma in armamento.ARMAS:
            return arma

        print("Arma no válida. Elija una de las armas disponibles.")

def pedir_eje(arma):
    """Pide el eje cuando el arma lo necesita.

    Recibe:
        arma: letra del arma seleccionada.

    Devuelve:
        El eje elegido o None si no corresponde.
    """
    if arma == "L":
        opciones = "x o y"
        patron = r"^[xy]$"
    else:
        return None

    while True:
        eje = input(f"Elegí el eje ({opciones}): ").strip().lower()

        if re.match(patron, eje):
            return eje

        print("Eje no válido.")


def pedir_objetivo(n_max):
    """Pide y valida las coordenadas del objetivo.

    Recibe:
        n_max: tamaño del cubo.

    Devuelve:
        Una tupla con las coordenadas (z, x, y).
    """
    while True:
        entrada = input("Objetivo (z,x,y): ").strip()
        coincidencia = re.match(PATRON_OBJETIVO, entrada)

        if not coincidencia:
            print("Formato inválido. Use z,x,y (ejemplo: 4,7,2).")
            continue

        z, x, y = [int(valor) for valor in coincidencia.groups()]

        if 1 <= z <= n_max and 1 <= x <= n_max and 1 <= y <= n_max:
            return (z, x, y)

        print(f"Las coordenadas deben estar entre 1 y {n_max}.")




def nueva_partida_1v1(configuracion):
    """
    Crea el estado inicial de una partida entre dos jugadores.

    Recibe:
        configuracion: diccionario con la configuración.

    Devuelve:
        El estado inicial de la partida.
    """
    n_max = configuracion.get("n", 8)

    cubo_jugador_1 = tablero.crear_cubo(n_max)
    cubo_jugador_2 = tablero.crear_cubo(n_max)

    flota_jugador_1 = flota.ubicacion_automatica(
        cubo_jugador_1, flota.CATALOGO_NAVES, 1
    )

    flota_jugador_2 = flota.ubicacion_automatica(
        cubo_jugador_2, flota.CATALOGO_NAVES, 2
    )

    estado = {
        "n_max": n_max,
        "turno_actual": 1,
        "modo": "1v1",
        "jugadores": {
            1: {
                "nombre": "Jugador 1",
                "cubo": cubo_jugador_1,
                "flota": flota_jugador_1,
                "municion": armamento.municion_inicial(),
                "disparos": set()
            },
            2: {
                "nombre": "Jugador 2",
                "cubo": cubo_jugador_2,
                "flota": flota_jugador_2,
                "municion": armamento.municion_inicial(),
                "disparos": set()
            }
        },
        "ganador": None
    }

    return estado

def nueva_partida_vs_maquina(configuracion, dificultad="facil"):
    """Crea el estado inicial de una partida contra la máquina.

    Recibe:
        configuracion: configuración de la partida.
        dificultad: nivel de la máquina.

    Devuelve:
        El estado inicial de la partida.
    """
    estado = nueva_partida_1v1(configuracion)

    estado["modo"] = "vs_maquina"
    estado["dificultad"] = dificultad
    estado["jugadores"][2]["nombre"] = "Máquina"

    return estado


def hay_ganador(estado):
    """Comprueba si algún jugador hundió toda la flota rival.

    Recibe:
        estado: estado actual de la partida.

    Devuelve:
        El nombre del ganador o None si no hay ganador.
    """
    for id_jugador in (1, 2):
        id_rival = 2 if id_jugador == 1 else 1
        flota_rival = estado["jugadores"][id_rival]["flota"]

        if flota_rival:
            todas_hundidas = all(
                nave.get("hundida", False) for nave in flota_rival
            )

            if todas_hundidas:
                return estado["jugadores"][id_jugador]["nombre"]

    return None


def es_turno_maquina(estado):
    """Indica si el jugador actual es la máquina.

    Recibe:
        estado: estado actual de la partida.

    Devuelve:
        True si juega la máquina; False en caso contrario.
    """
    return (
        estado["modo"] == "vs_maquina"
        and estado["turno_actual"] == 2
    )


def turno_maquina(estado):
    """Genera y ejecuta un disparo aleatorio de la máquina.

    Recibe:
        estado: estado actual de la partida.

    Devuelve:
        El estado actualizado después del turno.
    """
    n = estado["n_max"]
    actual = estado["turno_actual"]

    objetivos_disponibles = []

    for z in range(1, n + 1):
        for x in range(1, n + 1):
            for y in range(1, n + 1):
                punto = (z, x, y)

                if punto not in estado["jugadores"][actual]["disparos"]:
                    objetivos_disponibles.append(punto)

    if not objetivos_disponibles:
        print("La máquina no tiene objetivos disponibles.")
        return estado

    disparo = random.choice(objetivos_disponibles)

    jugada = {
        "arma": "T",
        "objetivo": disparo,
        "eje": None
    }

    print(f"La máquina dispara a {disparo}.")

    return ejecutar_turno(estado, jugada)


def ejecutar_turno(estado, jugada):
    """Ejecuta una jugada y actualiza el estado.

    Recibe:
        estado: estado actual de la partida.
        jugada: diccionario con arma, objetivo y eje.

    Devuelve:
        El estado actualizado.
    """
    actual = estado["turno_actual"]
    rival = 2 if actual == 1 else 1

    ganador = hay_ganador(estado)

    if ganador:
        estado["ganador"] = ganador
        return estado

    arma = jugada.get("arma")
    objetivo = jugada.get("objetivo")
    eje = jugada.get("eje")

    if arma not in armamento.ARMAS:
        print("El arma seleccionada no es válida.")
        return estado

    if arma == "L" and eje not in ("x", "y"):
        print("Para el láser debe elegir el eje x o y.")
        return estado

    if arma == "S" and eje not in ("z", "x", "y"):
        print("Para el sonar debe elegir el eje z, x o y.")
        return estado

    if not isinstance(objetivo, (tuple, list)) or len(objetivo) != 3:
        print("El objetivo no es válido.")
        return estado

    if any(
        not isinstance(coordenada, int)
        or isinstance(coordenada, bool)
        or coordenada < 1
        or coordenada > estado["n_max"]
        for coordenada in objetivo
    ):
        print("Las coordenadas están fuera del cubo.")
        return estado

    objetivo = tuple(objetivo)

    jugador = estado["jugadores"][actual]
    oponente = estado["jugadores"][rival]

    if objetivo in jugador["disparos"]:
        print("Ya disparaste a esa coordenada.")
        return estado

    ocupadas = set()

    for nave in oponente["flota"]:
        if not nave.get("hundida", False):
            for punto in nave.get("celdas", []):
                ocupadas.add(tuple(punto))

    resultado = armamento.aplicar_disparo(
        arma,
        oponente["cubo"],
        objetivo,
        ocupadas,
        jugador["municion"],
        eje
    )

    if not resultado["celdas"]:
        print("No se pudo realizar el disparo. Revisá la munición.")
        return estado

    for punto in resultado["celdas"]:
        punto = tuple(punto)
        jugador["disparos"].add(punto)

        z, x, y = punto

        if punto in resultado["impactos"]:
            oponente["cubo"][z - 1][y - 1][x - 1] = "I"

        elif punto in resultado["agua"]:
            oponente["cubo"][z - 1][y - 1][x - 1] = "A"

    for punto in resultado["impactos"]:
        punto = tuple(punto)

        for nave in oponente["flota"]:
            celdas_nave = [
                tuple(celda) for celda in nave.get("celdas", [])
            ]

            if punto in celdas_nave:
                impactos_nave = nave.setdefault("impactos", set())
                impactos_nave.add(punto)

                resistencia = nave.get(
                    "resistencia",
                    len(celdas_nave)
                )

                if len(impactos_nave) >= resistencia:
                    nave["hundida"] = True
                    print("¡Hundiste una nave!")

    print(f"Celdas afectadas: {len(resultado['celdas'])}")
    print(f"Impactos: {len(resultado['impactos'])}")
    print(f"Agua: {len(resultado['agua'])}")

    ganador = hay_ganador(estado)

    if ganador:
        estado["ganador"] = ganador
        print(f"¡Ganó {ganador}!")
    else:
        estado["turno_actual"] = rival

    return estado
