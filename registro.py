def estadistica(historial, jugador): 
     """Cuenta las jugadas de cada jugador.

    Recibe: historial (lista de jugadas).
    Devuelve: diccionario {jugador: {"disparos", "impactos", "aguas"}}.
    Lanza: nada.
    """
    resultado = {}
    for accion in historial:
        jugador = accion["jugador"]
        if jugador not in resultado:
            resultado[jugador] = {"disparos": 0, "impactos": 0, "aguas": 0}
        resultado[jugador]["disparos"] += 1
    return resultado 


def resumen_final(historial, ganador):
    """Arma el texto del resumen al terminar la partida.

    Recibe: historial (lista de jugadas) y ganador (str).
    Devuelve: texto (str) para que el integrador lo imprima.
    Lanza: nada.
    """
    resultado = estadisticas(historial)
    texto = "===== RESUMEN DE LA PARTIDA =====\n"
    texto += "Turnos jugados: " + str(len(historial)) + "\n"
    texto += "Ganador: " + ganador + "\n"
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

