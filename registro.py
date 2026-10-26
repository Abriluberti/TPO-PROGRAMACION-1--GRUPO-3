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

