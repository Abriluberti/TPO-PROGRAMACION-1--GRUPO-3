def estadistica(historial, jugador=None):
    """Cuenta las jugadas de cada jugador.

    Recibe:
        historial: lista de jugadas.
        jugador: jugador específico o None para todos.

    Devuelve:
        Diccionario con disparos, impactos y aguas.
    """
    resultado = {}

    for accion in historial:
        nombre = accion["jugador"]

        if jugador is not None and nombre != jugador:
            continue

        if nombre not in resultado:
            resultado[nombre] = {
                "disparos": 0,
                "impactos": 0,
                "aguas": 0
            }

        resultado[nombre]["disparos"] += 1

        if accion["resultado"] == "impacto":
            resultado[nombre]["impactos"] += 1
        elif accion["resultado"] == "agua":
            resultado[nombre]["aguas"] += 1

    return resultado


def resumen_final(historial, ganador):
    """Arma el texto del resumen al terminar la partida.

    Recibe:
        historial: lista de jugadas.
        ganador: nombre del ganador.

    Devuelve:
        Texto con el resumen de la partida.
    """
    resultado = estadistica(historial)

    texto = "===== RESUMEN DE LA PARTIDA =====\n"
    texto += "Turnos jugados: " + str(len(historial)) + "\n"
    texto += "Ganador: " + str(ganador) + "\n"

    for jugador in resultado:
        datos = resultado[jugador]
        texto += jugador + ": " + str(datos["disparos"]) + " disparos, "
        texto += str(datos["impactos"]) + " impactos, "
        texto += str(datos["aguas"]) + " aguas\n"

    return texto

def crear_historial ():
    return []

def registro (historial, jugador, arma, objetivo, resultado):
    accion= {
        "jugador": jugador,
        "arma": arma,
        "objetivo": objetivo,
        "resultado": resultado
    }
    historial.append(accion)
    return historial

