
import random
import armamento
import tablero
import flota
import re
import partida

PATRON_ARMA = r"^[TRCLOG]$"
PATRON_OBJETIVO = r"^(\d+),(\d+),(\d+)$"

def ejecutar_menu_principal():
    """Muestra el menú principal en ciclo y despacha la opción elegida con un diccionario.

    Recibe:
        Ningún parámetro.

    Devuelve:
        None al seleccionar la opción de salida.
    """
    rutas_menu = {
        "1": opcion_1v1,
        "2": opcion_vs_maquina,
        "3": opcion_maquina_vs_maquina,
        "4": opcion_continuar,
        "5": opcion_salir
    }

    continuar = True
    while continuar == True:
        print("===== OPERACION CUBO =====")
        print("1 - Partida uno contra uno")
        print("2 - Partida uno contra la maquina")
        print("3 - Partida maquina contra maquina")
        print("4 - Continuar una partida guardada")
        print("5 - Salir")

        opcion = pedir_opcion_menu(
            ["1", "2", "3", "4", "5"],
            "Opcion: ",
            "Opcion invalida. Ingrese un numero entre 1 y 5"
        )

        accion = rutas_menu.get(opcion)

        if accion != None:
            continuar = accion()


def pedir_arma():
    """
    Pide y valida el arma seleccionada.
    Devuelve la letra del arma elegida.
    """

    return pedir_opcion_menu(
        ["T", "R", "C", "L", "O", "G"],
        "Arma (T/R/C/L/O/G): ",
        "Arma no válida. Elija una de las armas disponibles.",
        True
    )


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

    modo_jugador_1 = pedir_opcion_menu(
        ["1", "2"],
        "Ubicacion jugador 1 (Manual: 1, Automatica: 2): ",
        "El modo de ubicacion es invalido."
    )

    modo_jugador_2 = pedir_opcion_menu(
        ["1", "2"],
        "Ubicacion jugador 2 (Manual: 1, Automatica: 2): ",
        "El modo de ubicacion es invalido."
    )

    # OJO: ubicacion_manual/ubicacion_automatica devuelven (cubo, flota),
    # no solo la flota. Antes se pisaba flota_jugador_x con la tupla entera
    # y de ahi en adelante todo lo que esperaba una lista de naves rompia.
    if modo_jugador_1 == "1":
        cubo_jugador_1, flota_jugador_1 = flota.ubicacion_manual(
            cubo_jugador_1, flota.CATALOGO_NAVES, 1
        )
    else:
        cubo_jugador_1, flota_jugador_1 = flota.ubicacion_automatica(
            cubo_jugador_1, flota.CATALOGO_NAVES, 1
        )

    if modo_jugador_2 == "1":
        cubo_jugador_2, flota_jugador_2 = flota.ubicacion_manual(
            cubo_jugador_2, flota.CATALOGO_NAVES, 2
        )
    else:
        cubo_jugador_2, flota_jugador_2 = flota.ubicacion_automatica(
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
                "disparos": set(),
                # celdas propias que el rival ya impacto, se usa para
                # saber si una nave se hundio y si se gano la partida
                "impactos_recibidos": set()
            },
            2: {
                "nombre": "Jugador 2",
                "cubo": cubo_jugador_2,
                "flota": flota_jugador_2,
                "municion": armamento.municion_inicial(),
                "disparos": set(),
                "impactos_recibidos": set()
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


def nueva_partida_maquina_vs_maquina(configuracion, dificultades=("facil", "facil")):
    """Crea el estado inicial de una partida entre dos máquinas.

    Recibe:
        configuracion: configuración de la partida.
        dificultades: nivel de cada máquina (jugador 1 y jugador 2).

    Devuelve:
        El estado inicial de la partida.
    """
    # esta funcion faltaba por completo: opcion_maquina_vs_maquina() ya
    # la llamaba pero no existia, tiraba AttributeError al elegir la
    # opcion 3 del menu.
    estado = nueva_partida_1v1(configuracion)

    estado["modo"] = "maquina_vs_maquina"
    estado["dificultad"] = dificultades
    estado["jugadores"][1]["nombre"] = "Máquina 1"
    estado["jugadores"][2]["nombre"] = "Máquina 2"

    return estado


def hay_ganador(estado):
    """Comprueba si algún jugador hundió toda la flota rival.

    Recibe:
        estado: estado actual de la partida.

    Devuelve:
        El nombre del ganador o None si no hay ganador.
    """
    for id_jugador in (1, 2):
        id_rival = 3 - id_jugador

        flota_rival = estado["jugadores"][id_rival]["flota"]
        impactos_rival = estado["jugadores"][id_rival]["impactos_recibidos"]

        # las naves nunca se borran de la flota (flota.py no las saca de
        # la lista), asi que "todo hundido" significa que cada celda de
        # cada nave ya fue impactada, no que la lista este vacia
        celdas_rival = [tuple(celda) for nave in flota_rival for celda in nave]

        if celdas_rival and all(celda in impactos_rival for celda in celdas_rival):
            return estado["jugadores"][id_jugador]["nombre"]

    return None


def es_turno_maquina(estado):
    """Indica si el jugador actual es la máquina.

    Recibe:
        estado: estado actual de la partida.

    Devuelve:
        True si juega la máquina; False en caso contrario.
    """
    if estado["modo"] == "maquina_vs_maquina":
        return True

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


def _adaptar_flota(flota_jugador, impactos_recibidos):
    """Convierte la flota (listas de celdas, formato de flota.py) al
    formato de nave con diccionario que espera armamento.py (celdas,
    impactos, hundida). Se usa solo para pasarsela a armamento, el
    estado real de la partida sigue guardando la flota como listas.
    """
    naves_adaptadas = []

    for celdas_nave in flota_jugador:
        celdas = {tuple(celda) for celda in celdas_nave}
        impactos = celdas & impactos_recibidos

        naves_adaptadas.append({
            "celdas": celdas,
            "impactos": impactos,
            "hundida": impactos == celdas
        })

    return naves_adaptadas


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

    if arma == "G":
        # las naves son listas de celdas (no diccionarios), asi que el
        # impacto previo se busca contra impactos_recibidos directamente.
        # Ademas descartamos las naves ya hundidas: si todas sus celdas
        # estan impactadas, no sirven como blanco del torpedo guiado.
        celdas_validas_para_guiado = set()

        for nave in oponente["flota"]:
            celdas_nave = {tuple(punto) for punto in nave}
            impactos_nave = celdas_nave & oponente["impactos_recibidos"]

            if impactos_nave and impactos_nave != celdas_nave:
                celdas_validas_para_guiado |= impactos_nave

        if objetivo not in celdas_validas_para_guiado:
            print("El torpedo guiado necesita un impacto previo en una nave no hundida.")
            return estado

    elif objetivo in jugador["disparos"]:
        print("Ya disparaste a esa coordenada.")
        return estado

    ocupadas = set()

    for nave in oponente["flota"]:
        for punto in nave:
            ocupadas.add(tuple(punto))

    # armamento.py (torpedo_guiado) espera que cada nave sea un diccionario
    # con "celdas"/"impactos"/"hundida", pero en flota.py cada nave es
    # simplemente una lista de celdas. Se adapta aca para no modificar
    # ni armamento.py ni flota.py.
    flota_para_armamento = _adaptar_flota(oponente["flota"], oponente["impactos_recibidos"])

    resultado = armamento.aplicar_disparo(
        arma,
        oponente["cubo"],
        objetivo,
        ocupadas,
        jugador["municion"],
        eje,
        flota_para_armamento,
        jugador["disparos"]
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
            if punto in nave:
                oponente["impactos_recibidos"].add(punto)

                # antes esto tambien hacia nave["hundida"] = True, pero
                # nave es una lista de celdas, no un diccionario -> rompia
                # con TypeError en cuanto entraba un impacto. La nave ya
                # queda marcada como hundida de forma implicita cuando
                # todas sus celdas estan en impactos_recibidos.
                if all(tuple(celda) in oponente["impactos_recibidos"] for celda in nave):
                    print("¡Hundiste una nave!")
                break

    print(f"Celdas afectadas: {len(resultado['celdas'])}")
    print(f"Impactos: {len(resultado['impactos'])}")
    print(f"Agua: {len(resultado['agua'])}")

    ganador = hay_ganador(estado)

    if ganador:
        estado["ganador"] = ganador
        print(f"¡Ganó {ganador}!")
    else:
        estado["turno_actual"] = rival

    # se sacan los 3 planos que se imprimian despues de cada jugada
    # (ensuciaban la consola en cada turno; ademas los ejes estaban mal
    # pasados: dibujar_plano_x recibia objetivo[0], que es z, no x)

    return estado



# Funciones de validacion

def pedir_opcion_menu(opciones_validas, texto, texto_opcion_invalida, mayuscula = False):
    """Solicita y valida mediante expresiones regulares una opción numérica del menú.

    Recibe:
        texto_input: cadena de texto que se muestra al pedir el dato por consola.

    Devuelve:
        Cadena de texto con el número de opción validado entre 1 y 5.
    """

    opcion_seleccionada = ""

    while opcion_seleccionada == "":
        entrada = input_usuario(texto)

        if mayuscula:
            entrada = entrada.upper()

        if entrada in opciones_validas:
            opcion_seleccionada = entrada
        else:
            print(texto_opcion_invalida)

    return opcion_seleccionada

def input_usuario(texto):
    """Solicita y valida mediante expresiones regulares una opción numérica del menú.

    Recibe:
        texto_input: cadena de texto que se muestra al pedir el dato por consola.

    Devuelve:
        Cadena de texto con el número de opción validado entre 1 y 5.
    """
    return input(texto)

# Opciones del menu

def opcion_1v1():
    """Inicia y ejecuta una partida en formato uno contra uno.

    Recibe:
        Ningún parámetro.

    Devuelve:
        True al finalizar la partida para mantener activo el menú principal.
    """
    print("Iniciando Partida 1 contra 1...")

    estado = partida.nueva_partida_1v1({"n": 8})

    jugar_partida(estado)

    return True


def opcion_vs_maquina():
    """Inicia y ejecuta una partida en formato jugador contra la máquina.

    Recibe:
        Ningún parámetro.

    Devuelve:
        True al finalizar la partida para mantener activo el menú principal.
    """
    print("Iniciando Partida contra la maquina...")

    estado = partida.nueva_partida_vs_maquina({"n": 8})

    jugar_partida(estado)

    return True


def opcion_maquina_vs_maquina():
    """Inicia y ejecuta una partida en formato máquina contra máquina.

    Recibe:
        Ningún parámetro.

    Devuelve:
        True al finalizar la partida para mantener activo el menú principal.
    """
    print("Iniciando Partida maquina contra maquina...")

    estado = partida.nueva_partida_maquina_vs_maquina(
        {"n": 8},
        ["facil", "facil"]
    )

    jugar_partida(estado)

    return True
def opcion_continuar():
    """Permite buscar y retomar una partida guardada previamente.

    Recibe:
        Ningún parámetro.

    Devuelve:
        True para volver a mostrar el menú principal tras la operación.
    """
    print("Buscando partidas guardadas...")
    return True

def opcion_salir():
    """Finaliza la ejecución del menú principal y cierra el juego.

    Recibe:
        Ningún parámetro.

    Devuelve:
        False para indicar el corte del ciclo del menú principal.
    """
    print("Saliendo del juego...")
    return False


# Funcion para seleccionar opcion del menu




def jugar_partida(estado):
    """
    Gestiona el ciclo de turnos de una partida hasta que haya un ganador.

    Recibe:
        estado: diccionario con el estado actual de la partida (jugadores, turno y cubo).

    Devuelve:
        El diccionario de estado actualizado al finalizar la partida.
    """
    while estado["ganador"] is None:
        actual = estado["turno_actual"]
        jugador = estado["jugadores"][actual]

        print("\nTurno de", jugador["nombre"])

        # faltaba esto: si le toca a la maquina, que juegue sola.
        # antes siempre se le pedia arma/objetivo al humano, incluso
        # en el turno del jugador 2 cuando el modo era vs_maquina.
        if partida.es_turno_maquina(estado):
            estado = partida.turno_maquina(estado)
            continue

        arma = partida.pedir_arma()
        objetivo = partida.pedir_objetivo(estado["n_max"])

        jugada = {
            "arma": arma,
            "objetivo": objetivo
        }

        if arma in ("L", "S"):
            jugada["eje"] = partida.pedir_eje(arma)

        estado = partida.ejecutar_turno(estado, jugada)

    print("Ganador:", estado["ganador"])
    return estado