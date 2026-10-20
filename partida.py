import re
import random

PATRON_MENU_TURNO = r"^[1-3]$"
PATRON_ARMA = r"^[TRCLS]$"
PATRON_OBJETIVO = r"^([1-9]),([1-9]),([1-9])$"
PATRON_EJE = r"^[zxy]$"

def pedir_arma():
    while True:
        arma = input("Arma (T/R/C/S/L): ").strip().upper()
        if re.match(PATRON_ARMA, arma):
            return arma
        print("Arma no valida. Elija entre T, R, C, S o L.")


def pedir_objetivo(n_max):
    while True:
        entrada = input("Objetivo (z,x,y): ").strip()
        match = re.match(PATRON_OBJETIVO, entrada)
        if not match:
            print("Formato invalido. Debe ser z,x,y (ej: 4,2,7).")
            continue

        z, x, y = [int(v) for v in match.groups()]
        if 1 <= z <= n_max and 1 <= x <= n_max and 1 <= y <= n_max:
            return (z, x, y)
        print(f"Coordenadas fuera de rango. Deben estar entre 1 y {n_max}.")


def nueva_partida_1v1(configuracion):
    n_max = configuracion.get("n", 8)
    return {
        "n_max": n_max,
        "turno_actual": 1,
        "modo": "1v1",
        "jugadores": {
            1: {"nombre": "Jugador 1", "cubo": None, "flota": []},
            2: {"nombre": "Jugador 2", "cubo": None, "flota": []}
        },
        "ganador": None
    }


def nueva_partida_vs_maquina(configuracion, dificultad="facil"):
    estado = nueva_partida_1v1(configuracion)
    estado["modo"] = "vs_maquina"
    estado["dificultad"] = dificultad
    estado["jugadores"][2]["nombre"] = "Máquina"
    return estado


def hay_ganador(estado):
     #revisa si quedan flotas del jugador
    for id_rival, id_oponente in ((1, 2), (2, 1)):
        flota_rival = estado["jugadores"][id_rival]["flota"]
        if flota_rival:
            todas_hundidas = all(nave.get("hundida", False) for nave in flota_rival)
            if todas_hundidas:
                return estado["jugadores"][id_oponente]["nombre"]
    return None


def turno_maquina(estado):
    n = estado["n_max"]
    # Coordenadas aleatorias
    disparo = (random.randint(1, n), random.randint(1, n), random.randint(1, n))
    jugada = {
        "arma": "T",
        "objetivo": disparo
    }
    print(f"\n--- Turno de la máquina ---")
    print(f"Dispara a {disparo[0]},{disparo[1]},{disparo[2]}.")
    
    return ejecutar_turno(estado, jugada)


def ejecutar_turno(estado, jugada):
    actual = estado["turno_actual"]
    rival = 2 if actual == 1 else 1
    ganador = hay_ganador(estado)
    if ganador:
        estado["ganador"] = ganador
        return estado
    