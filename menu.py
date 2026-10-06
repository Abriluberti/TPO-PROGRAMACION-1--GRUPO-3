import re

# Funciones de Validacion

def pedir_opcion_menu(texto_input, limite_opciones=5):
    patron = rf"^[1-{limite_opciones}]$"                            # Aca con rf asignamos los parametros que se pueden usar [1-5]
    while True:
        entrada = input(texto_input)
        if re.match(patron, entrada):
            return entrada
        print("Opcion invalida. Ingrese un numero entre 1 y ", limite_opciones)


# Opciones del menu

def opcion_1v1():
    print("Iniciando Partida 1 contra 1...")
    return True


def opcion_vs_maquina():
    print("Iniciando Partida contra la maquina...")
    return True


def opcion_maquina_vs_maquina():
    print("Iniciando Partida maquina contra maquina...")
    return True


def opcion_continuar():
    print("Buscando partidas guardadas...")
    return True


def opcion_salir():
    print("Saliendo del juego...")
    return False                         # Aca retorna false para cortar el bucle principal


# Funcion para seleccionar opcion del menu

def ejecutar_menu_principal():

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
        
        accion = rutas_menu.get(opcion)          # Usamos get para que devuelva none en caso de no estar la opcion en lugar de error
        
        if accion != None:
            continuar = accion()


# Bloque para poder probarlo directamente
if __name__ == "__main__":
    ejecutar_menu_principal()