"""Módulo armamento: catálogo de armas y disparo.

No usa print ni input: recibe datos y devuelve datos.
Los puntos son tuplas (z, x, y).
"""


cargar_armamento = {
    "T": {
        "nombre": "torpedo",
        "municion": None
    },
    "R": {
        "nombre": "misil de racimo",
        "municion": 3
    },
    "C": {
        "nombre": "carga de profundidad",
        "municion": 2
    },
    "S": {
        "nombre": "sonar",
        "municion": 4
    },
    "L": {
        "nombre": "barrido laser",
        "municion": 2
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


def torpedo(cubo, punto):
    """Celdas que afecta el torpedo: solo la apuntada.

    Recibe:
        cubo: lista de listas de listas.
        punto: tupla (z, x, y).

    Devuelve:
        Conjunto con el punto apuntado.

    Lanza:
        Nada.
    """

    return {punto}