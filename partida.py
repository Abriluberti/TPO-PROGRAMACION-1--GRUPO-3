
import random
import armamento
import tablero
import flota
import radar
import registro
import re
import partida

PATRON_OBJETIVO = r"^(\d+),(\d+),(\d+)$"
PATRON_TRAMO = r"^(\d+),(\d+),(\d+)-(\d+),(\d+),(\d+)$"

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
        ["T", "R", "C", "L", "O", "G", "S"],
        "Arma (T/R/C/L/O/G/S): ",
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
    if arma in ("L", "S"):
        opciones = "x o y" if arma == "L" else "z, x o y"
        patron = r"^[xy]$" if arma == "L" else r"^[zxy]$"
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


def _pedir_tramo(n_max):
    """Pide el tramo de una nave en formato Desde-Hasta (z,x,y-z,x,y).

    Recibe:
        n_max: tamaño del cubo.

    Devuelve:
        (punto_desde, punto_hasta), cada uno una tupla (z, x, y).
    """
    while True:
        entrada = input("Desde-hasta (ej: 3,5,4-3,5,5): ").strip()
        coincidencia = re.match(PATRON_TRAMO, entrada)

        if not coincidencia:
            print("Formato inválido. Use z,x,y-z,x,y (ejemplo: 3,5,4-3,5,5).")
            continue

        valores = [int(valor) for valor in coincidencia.groups()]

        if not all(1 <= valor <= n_max for valor in valores):
            print(f"Las coordenadas deben estar entre 1 y {n_max}.")
            continue

        return tuple(valores[:3]), tuple(valores[3:])


def _ubicar_flota_manual(cubo, n_max):
    """Pide por consola la ubicacion manual de toda la flota de un jugador.

    Recibe:
        cubo: cubo vacío del jugador.
        n_max: tamaño del cubo.

    Devuelve:
        (cubo, flota) con todas las naves del catálogo ubicadas.
    """
    flota_jugador = []
    total_naves = sum(datos["cantidad"] for datos in flota.CATALOGO_NAVES.values())

    while len(flota_jugador) < total_naves:
        letras_pendientes = [
            letra for letra, datos in flota.CATALOGO_NAVES.items()
            if sum(1 for nave in flota_jugador if nave["letra"] == letra) < datos["cantidad"]
        ]

        pendientes = ", ".join(
            f"{letra} x{datos['cantidad'] - sum(1 for nave in flota_jugador if nave['letra'] == letra)}"
            for letra, datos in flota.CATALOGO_NAVES.items()
            if letra in letras_pendientes
        )
        print(f"Pendientes: {pendientes}")

        letra = pedir_opcion_menu(
            letras_pendientes,
            "Nave (" + "/".join(flota.CATALOGO_NAVES.keys()) + "): ",
            "Nave inválida.",
            True
        )

        punto_desde, punto_hasta = _pedir_tramo(n_max)

        try:
            cubo, flota_jugador = flota.ubicar_nave(
                cubo, flota_jugador, letra, punto_desde, punto_hasta
            )
        except flota.FlotaError as error:
            print(f"No se puede ubicar ahi: {error}")
        else:
            print("Ubicada.")

    return cubo, flota_jugador


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

    if modo_jugador_1 == "1":
        cubo_jugador_1, flota_jugador_1 = _ubicar_flota_manual(cubo_jugador_1, n_max)
    else:
        cubo_jugador_1, flota_jugador_1 = flota.ubicacion_automatica(
            cubo_jugador_1, flota.CATALOGO_NAVES
        )

    if modo_jugador_2 == "1":
        cubo_jugador_2, flota_jugador_2 = _ubicar_flota_manual(cubo_jugador_2, n_max)
    else:
        cubo_jugador_2, flota_jugador_2 = flota.ubicacion_automatica(
            cubo_jugador_2, flota.CATALOGO_NAVES
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
        "historial": [],
        "ganador": None
    }

    return estado

def nueva_partida_vs_maquina(configuracion, dificultad="facil"):
    """Crea el estado inicial de una partida contra la máquina.

    Recibe:
        configuracion: configuración de la partida.
        dificultad: nivel de la máquina ("facil" o "dificil").

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
    estado = nueva_partida_1v1(configuracion)

    estado["modo"] = "maquina_vs_maquina"
    estado["dificultad"] = tuple(dificultades)
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

        if flota_rival and all(nave["hundida"] for nave in flota_rival):
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
    """Genera y ejecuta la jugada de la máquina según su dificultad.

    facil: dispara con torpedo a una celda al azar no disparada antes.
    dificil: si ya impactó una nave rival sin hundirla, la remata con
        torpedo guiado; si no, dispara al azar como en facil.

    Recibe:
        estado: estado actual de la partida.

    Devuelve:
        El estado actualizado después del turno.
    """
    n = estado["n_max"]
    actual = estado["turno_actual"]
    rival = 2 if actual == 1 else 1
    jugador = estado["jugadores"][actual]
    oponente = estado["jugadores"][rival]

    dificultad = estado.get("dificultad", "facil")
    if isinstance(dificultad, (list, tuple)):
        dificultad = dificultad[actual - 1]

    if dificultad == "dificil":
        for nave in oponente["flota"]:
            if nave["impactos"] and not nave["hundida"]:
                objetivo = next(iter(nave["impactos"]))
                print(f"La máquina remata con torpedo guiado a {objetivo}.")
                return ejecutar_turno(estado, {"arma": "G", "objetivo": objetivo, "eje": None})

    objetivos_disponibles = [
        (z, x, y)
        for z in range(1, n + 1)
        for x in range(1, n + 1)
        for y in range(1, n + 1)
        if (z, x, y) not in jugador["disparos"]
    ]

    if not objetivos_disponibles:
        print("La máquina no tiene objetivos disponibles.")
        return estado

    disparo = random.choice(objetivos_disponibles)
    print(f"La máquina dispara a {disparo}.")

    return ejecutar_turno(estado, {"arma": "T", "objetivo": disparo, "eje": None})


def _marcar_hundida(cubo, nave):
    """Marca en el cubo las celdas de una nave recién hundida."""
    for z, x, y in nave["celdas"]:
        cubo[z - 1][y - 1][x - 1] = tablero.HUNDIDO


def _revelar_celda_destructor(oponente):
    """Comportamiento propio del Destructor: al ser impactado revela
    una celda ocupada del rival (de cualquier nave no hundida).

    Recibe: oponente (jugador dueño de la flota atacada).
    Devuelve: None. Imprime la celda revelada, si queda alguna.
    """
    celdas_sin_revelar = set()

    for nave in oponente["flota"]:
        celdas_sin_revelar |= (nave["celdas"] - nave["impactos"])

    if celdas_sin_revelar:
        celda = random.choice(sorted(celdas_sin_revelar))
        print(f"¡El destructor averiado revela una celda ocupada del rival!: {celda}")


def _aplicar_bonus_estacion(estado, actual, nave):
    """Comportamiento propio de la Estación orbital: al hundirse otorga
    munición extra al jugador que la hundió.

    Recibe: estado, actual (id del jugador que disparó), nave hundida.
    Devuelve: None.
    """
    if nave["letra"] != "E":
        return

    municion = estado["jugadores"][actual]["municion"]
    for letra_arma in ("R", "C", "L"):
        if municion.get(letra_arma) is not None:
            municion[letra_arma] += 1

    print("¡La estación hundida otorga munición extra!")


def _ejecutar_sonar(estado, objetivo, eje):
    """Resuelve un turno de Sonar: no hace daño, revela un plano entero.

    Recibe:
        estado: estado de la partida.
        objetivo: tupla (z, x, y); solo se usa la coordenada del eje
            elegido como "valor" del plano.
        eje: "z", "x" o "y".

    Devuelve:
        El estado actualizado.
    """
    actual = estado["turno_actual"]
    rival = 2 if actual == 1 else 1
    jugador = estado["jugadores"][actual]
    oponente = estado["jugadores"][rival]

    if eje not in ("z", "x", "y"):
        print("Para el sonar debe elegir el eje z, x o y.")
        return estado

    if not isinstance(objetivo, (tuple, list)) or len(objetivo) != 3:
        print("El objetivo no es válido.")
        return estado

    if not armamento.tiene_municion("S", jugador["municion"]):
        print("No te queda munición de sonar.")
        return estado

    valor = objetivo[{"z": 0, "x": 1, "y": 2}[eje]]

    try:
        contactos, metricas = radar.sonar_plano(oponente["cubo"], eje, valor)
    except ValueError as error:
        print(f"No se pudo usar el sonar: {error}")
        return estado

    armamento.gastar_municion("S", jugador["municion"])

    for z, x, y in contactos:
        oponente["cubo"][z - 1][y - 1][x - 1] = tablero.DETECTADO_SONAR

    print(f"Sonar sobre el plano {eje} = {valor}. {len(contactos)} contactos detectados.")

    estado["historial"].append({
        "jugador": jugador["nombre"],
        "arma": "S",
        "objetivo": tuple(objetivo),
        "resultado": "contactos" if contactos else "sin contactos"
    })

    estado["turno_actual"] = rival
    return estado


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

    if arma == "S":
        return _ejecutar_sonar(estado, objetivo, eje)

    if arma not in armamento.ARMAS:
        print("El arma seleccionada no es válida.")
        return estado

    if arma == "L" and eje not in ("x", "y"):
        print("Para el láser debe elegir el eje x o y.")
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
        # las naves ya trackean sus propios impactos; el torpedo guiado
        # necesita una celda impactada de una nave que no este hundida
        celdas_validas_para_guiado = set()

        for nave in oponente["flota"]:
            if nave["impactos"] and not nave["hundida"]:
                celdas_validas_para_guiado |= nave["impactos"]

        if objetivo not in celdas_validas_para_guiado:
            print("El torpedo guiado necesita un impacto previo en una nave no hundida.")
            return estado

    elif objetivo in jugador["disparos"]:
        print("Ya disparaste a esa coordenada.")
        return estado

    ocupadas = set()
    for nave in oponente["flota"]:
        ocupadas |= nave["celdas"]

    # comportamiento propio del submarino: el barrido laser no lo alcanza
    if arma == "L":
        for nave in oponente["flota"]:
            if nave["letra"] == "S":
                ocupadas = ocupadas - nave["celdas"]

    resultado = armamento.aplicar_disparo(
        arma,
        oponente["cubo"],
        objetivo,
        ocupadas,
        jugador["municion"],
        eje,
        oponente["flota"],
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
            oponente["cubo"][z - 1][y - 1][x - 1] = tablero.IMPACTO

        elif punto in resultado["agua"]:
            oponente["cubo"][z - 1][y - 1][x - 1] = tablero.AGUA_MARCADA

    for punto in resultado["impactos"]:
        punto = tuple(punto)

        for nave in oponente["flota"]:
            if punto in nave["celdas"]:
                ya_estaba_impactada = punto in nave["impactos"]
                nave["impactos"].add(punto)

                if not ya_estaba_impactada and nave["letra"] == "D":
                    _revelar_celda_destructor(oponente)

                if not nave["hundida"] and nave["impactos"] == nave["celdas"]:
                    nave["hundida"] = True
                    print("¡Hundiste una nave!")
                    _marcar_hundida(oponente["cubo"], nave)
                    _aplicar_bonus_estacion(estado, actual, nave)

                break

    print(f"Celdas afectadas: {len(resultado['celdas'])}")
    print(f"Impactos: {len(resultado['impactos'])}")
    print(f"Agua: {len(resultado['agua'])}")

    if objetivo in resultado["impactos"]:
        resultado_jugada = "impacto"
    elif objetivo in resultado["agua"]:
        resultado_jugada = "agua"
    else:
        resultado_jugada = "sin_impacto_directo"

    estado["historial"].append({
        "jugador": jugador["nombre"],
        "arma": arma,
        "objetivo": objetivo,
        "resultado": resultado_jugada
    })

    ganador = hay_ganador(estado)

    if ganador:
        estado["ganador"] = ganador
        print(f"¡Ganó {ganador}!")
    else:
        estado["turno_actual"] = rival

    return estado


# Funciones de guardado y carga (usan registro.py, que trabaja con JSON
# y no soporta sets ni tuplas; aca se convierten en listas y de vuelta).

def _estado_para_guardar(estado):
    """Convierte el estado a una versión con solo tipos que soporta JSON.

    Recibe: estado (con sets y claves de jugador como enteros).
    Devuelve: un diccionario nuevo, listo para registro.guardar_partida.
    """
    jugadores = {}

    for id_jugador, jugador in estado["jugadores"].items():
        jugadores[str(id_jugador)] = {
            "nombre": jugador["nombre"],
            "cubo": jugador["cubo"],
            "flota": [
                {
                    "letra": nave["letra"],
                    "celdas": [list(celda) for celda in nave["celdas"]],
                    "impactos": [list(celda) for celda in nave["impactos"]],
                    "hundida": nave["hundida"]
                }
                for nave in jugador["flota"]
            ],
            "municion": jugador["municion"],
            "disparos": [list(punto) for punto in jugador["disparos"]]
        }

    return {
        "n_max": estado["n_max"],
        "turno_actual": estado["turno_actual"],
        "modo": estado["modo"],
        "dificultad": estado.get("dificultad"),
        "jugadores": jugadores,
        "historial": estado.get("historial", []),
        "ganador": estado["ganador"]
    }


def _estado_desde_guardado(datos):
    """Hace el camino inverso de _estado_para_guardar.

    Recibe: diccionario leído de un archivo guardado.
    Devuelve: estado de partida con sets, tuplas y claves int reconstruidos.
    """
    jugadores = {}

    for id_texto, jugador in datos["jugadores"].items():
        jugadores[int(id_texto)] = {
            "nombre": jugador["nombre"],
            "cubo": jugador["cubo"],
            "flota": [
                {
                    "letra": nave["letra"],
                    "celdas": {tuple(celda) for celda in nave["celdas"]},
                    "impactos": {tuple(celda) for celda in nave["impactos"]},
                    "hundida": nave["hundida"]
                }
                for nave in jugador["flota"]
            ],
            "municion": jugador["municion"],
            "disparos": {tuple(punto) for punto in jugador["disparos"]}
        }

    return {
        "n_max": datos["n_max"],
        "turno_actual": datos["turno_actual"],
        "modo": datos["modo"],
        "dificultad": datos.get("dificultad"),
        "jugadores": jugadores,
        "historial": datos.get("historial", []),
        "ganador": datos["ganador"]
    }


# Funciones de validacion

def pedir_opcion_menu(opciones_validas, texto, texto_opcion_invalida, mayuscula = False):
    """Solicita y valida mediante una expresión regular una opción de un menú.

    Recibe:
        opciones_validas: lista de cadenas aceptadas.
        texto: texto que se muestra al pedir el dato por consola.
        texto_opcion_invalida: mensaje si no coincide con ninguna opción.
        mayuscula: si True, convierte la entrada a mayúsculas antes de
            validar (para letras de armas y de naves).

    Devuelve:
        La opción elegida, tal como figura en opciones_validas.
    """
    patron = "^(" + "|".join(re.escape(opcion) for opcion in opciones_validas) + ")$"

    while True:
        entrada = input_usuario(texto)

        if mayuscula:
            entrada = entrada.upper()

        if re.match(patron, entrada):
            return entrada

        print(texto_opcion_invalida)

def input_usuario(texto):
    """Pide un dato de texto por consola.

    Recibe:
        texto: cadena que se muestra al pedir el dato por consola.

    Devuelve:
        La cadena tipeada por el usuario.
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

    dificultad = pedir_opcion_menu(
        ["1", "2"],
        "Dificultad de la maquina (Facil: 1, Dificil: 2): ",
        "La dificultad es invalida."
    )

    estado = partida.nueva_partida_vs_maquina(
        {"n": 8},
        "facil" if dificultad == "1" else "dificil"
    )

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
        ("facil", "facil")
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
    try:
        nombres = registro.listar_partidas()
    except registro.RegistroError as error:
        print(f"No se pudo leer el listado de partidas: {error}")
        return True

    if not nombres:
        print("No hay partidas guardadas.")
        return True

    print("Partidas guardadas:", ", ".join(nombres))
    nombre = input("Nombre de la partida a continuar (vacío para cancelar): ").strip()

    if nombre == "":
        return True

    try:
        datos = registro.cargar_partida(nombre)
    except registro.RegistroError as error:
        print(f"No se pudo continuar la partida: {error}")
    else:
        estado = _estado_desde_guardado(datos)
        jugar_partida(estado)

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


def _pedir_opcion_turno():
    """Pide la acción del turno: disparar, ver el cubo o guardar y salir."""
    return pedir_opcion_menu(
        ["1", "2", "3"],
        "1 - Disparar / 2 - Ver el cubo / 3 - Guardar y salir\nOpcion: ",
        "Opcion invalida. Ingrese 1, 2 o 3."
    )


def _ver_cubo(jugador, n_max):
    """Muestra una capa del propio cubo del jugador (naves y golpes recibidos).

    Recibe: jugador (diccionario de estado), n_max (tamaño del cubo).
    Devuelve: None, imprime el plano pedido.
    """
    z = pedir_opcion_menu(
        [str(valor) for valor in range(1, n_max + 1)],
        f"Capa z a mostrar (1 a {n_max}): ",
        f"Debe ser un número entre 1 y {n_max}."
    )
    print(tablero.dibujar_plano_z(jugador["cubo"], int(z)))


def _guardar_y_salir(estado):
    """Pide un nombre y guarda la partida con registro.guardar_partida.

    Recibe: estado de la partida en curso.
    Devuelve: None. No corta el programa si el nombre es inválido o no
        se puede escribir el archivo: registro.RegistroError se atrapa
        y se avisa por consola.
    """
    nombre = input("Nombre para guardar la partida: ").strip()

    try:
        registro.guardar_partida(_estado_para_guardar(estado), nombre)
    except registro.RegistroError as error:
        print(f"No se pudo guardar la partida: {error}")
    else:
        print(f"Partida '{nombre}' guardada.")
    finally:
        print("Volviendo al menú principal...")


def jugar_partida(estado):
    """
    Gestiona el ciclo de turnos de una partida hasta que haya un ganador.

    Recibe:
        estado: diccionario con el estado actual de la partida (jugadores, turno y cubo).

    Devuelve:
        El diccionario de estado actualizado al finalizar la partida (o
        al guardar y salir antes de que haya ganador).
    """
    while estado["ganador"] is None:
        actual = estado["turno_actual"]
        jugador = estado["jugadores"][actual]

        print("\n--- Turno de", jugador["nombre"], "---")

        if partida.es_turno_maquina(estado):
            estado = partida.turno_maquina(estado)
            continue

        opcion_turno = partida._pedir_opcion_turno()

        if opcion_turno == "2":
            partida._ver_cubo(jugador, estado["n_max"])
            continue

        if opcion_turno == "3":
            partida._guardar_y_salir(estado)
            return estado

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
