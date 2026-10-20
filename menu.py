import re    # Se importa la libreria re para poder asignar los parametros


# Validación de Opciones y asignacion de parametros

def pedir_opcion_menu(texto_input, limite_opciones=5):
    parametro = rf"^[1-{limite_opciones}]$"                      # Usamos "rf" para limitar las opciones solo entre [1-5]
    while True:
        entrada = input(texto_input)
        if re.match(parametro, entrada):                         # Usamos "if re.match" para verificar si el numero ingresado esta dentro del parametro
            return entrada
        print("Opción inválida. Ingrese un número entre 1 y ", limite_opciones)


# Bucle de repeticion y salida

def opcion_1v1():
    print("Iniciando Partida 1 contra 1...")
    return True


def opcion_vs_maquina():
    print("Iniciando Partida contra la máquina...")
    return True


def opcion_maquina_vs_maquina():
    print("Iniciando Partida máquina contra máquina...")
    return True


def opcion_continuar():
    print("Buscando partidas guardadas...")
    return True


def opcion_salir():
    print("Saliendo del juego...")
    return False                         # Aca arroja "flase" para salir del bucle


# Opciones del menu

def ejecutar_menu_principal():
    opciones_menu = {
        "1": opcion_1v1,
        "2": opcion_vs_maquina,
        "3": opcion_maquina_vs_maquina,
        "4": opcion_continuar,
        "5": opcion_salir
    }
    continuar = True
    while continuar == True:
        print(" ==== OPERACION CUBO ==== ")
        print("1 - Partida uno contra uno")
        print("2 - Partida uno contra la maquina")
        print("3 - Partida maquina contra maquina")
        print("4 - Continuar una partida guardada")
        print("5 - Salir")
        
        opcion = pedir_opcion_menu("Opcion: ", limite_opciones=5)
        
        accion = opciones_menu.get(opcion)         # Usamos "get" para que en caso de elegir un valor fuera del diccionario arroje "none" y no "KeyError"
        
        if accion != None:
            continuar = accion()


# Bloque para poder probarlo directamente
if __name__ == "__main__":
    ejecutar_menu_principal()