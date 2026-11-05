import re
import partida

# Funciones de validacion

def pedir_opcion_menu(texto_input, limite_opciones=5):
    """Solicita y valida mediante expresiones regulares una opción numérica del menú.

    Recibe:
        texto_input: cadena de texto que se muestra al pedir el dato por consola.
        limite_opciones: entero con la cantidad máxima de opciones válidas (por defecto 5).

    Devuelve:
        Cadena de texto con el número de opción validado entre 1 y limite_opciones.
    """
    patron = rf"^[1-{limite_opciones}]$"

    while True:
        entrada = input(texto_input)

        if re.match(patron, entrada):
            return entrada

        print(f"Opcion invalida. Ingrese un numero entre 1 y {limite_opciones}")

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

        opcion = pedir_opcion_menu("Opcion: ", limite_opciones=5)

        accion = rutas_menu.get(opcion)

        if accion != None:
            continuar = accion()



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
