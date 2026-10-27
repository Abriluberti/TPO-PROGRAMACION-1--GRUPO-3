import random
def colocar_fragata(cubo):
    """
    Recibe el cubo y solicita la posición de una fragata.
    Devuelve el cubo con la fragata ubicada.
    """

    n = len(cubo)

    while True:
        x = input("Elije la coordenada X de la proa de la Fragata: ")
        while not x.isdigit() or int(x) < 1 or int(x) > n:
            print("Error - Coordenada fuera del cubo")
            x = input("Elije la coordenada X entre 1 y " + str(n) + ": ")
        x = int(x) - 1

        y = input("Elije la coordenada Y de la proa de la Fragata: ")
        while not y.isdigit() or int(y) < 1 or int(y) > n:
            print("Error - Coordenada fuera del cubo")
            y = input("Elije la coordenada Y entre 1 y " + str(n) + ": ")
        y = int(y) - 1

        z = input("Elije la coordenada Z de la proa de la Fragata: ")
        while not z.isdigit() or int(z) < 1 or int(z) > n:
            print("Error - Coordenada fuera del cubo")
            z = input("Elije la coordenada Z entre 1 y " + str(n) + ": ")
        z = int(z) - 1

        if cubo[z][y][x] != "~":
            print("Error: ya hay una nave ocupando esa posición.")
            continue

        sentido = input("Elige 'vertical' u 'horizontal': ").strip().lower()

        while sentido != "vertical" and sentido != "horizontal":
            print("Error: ingrese un sentido válido")
            sentido = input("Elige 'vertical' u 'horizontal': ").strip().lower()

        if sentido == "vertical":
            direccion = input("Elige 'arriba' o 'abajo': ").strip().lower()

            while direccion != "arriba" and direccion != "abajo":
                print("Error: ingrese una dirección válida")
                direccion = input("Elige 'arriba' o 'abajo': ").strip().lower()

            if direccion == "arriba":
                celdas = [(z, y, x), (z, y - 1, x)]
            else:
                celdas = [(z, y, x), (z, y + 1, x)]

        else:
            direccion = input(
                "Elige 'derecha', 'izquierda', 'atras' o 'adelante': "
            ).strip().lower()

            while direccion not in ("derecha", "izquierda", "atras", "adelante"):
                print("Error: ingrese una dirección válida")
                direccion = input(
                    "Elige 'derecha', 'izquierda', 'atras' o 'adelante': "
                ).strip().lower()

            if direccion == "derecha":
                celdas = [(z, y, x), (z, y, x + 1)]
            elif direccion == "izquierda":
                celdas = [(z, y, x), (z, y, x - 1)]
            elif direccion == "atras":
                celdas = [(z, y, x), (z + 1, y, x)]
            else:
                celdas = [(z, y, x), (z - 1, y, x)]

        if posicion_valida(cubo, celdas):
            for z_celda, y_celda, x_celda in celdas:
                cubo[z_celda][y_celda][x_celda] = "?"
            return cubo

        print("Error: la fragata sale del cubo, ocupa una casilla ocupada o toca otra nave.")
        print("Intenta colocarla nuevamente.")

###############################################################################################################

def colocar_destructor(cubo):
    """
    Recibe el cubo y solicita la posición de un destructor.
    Devuelve el cubo con el destructor ubicado.
    """

    n = len(cubo)

    while True:
        x = input("Elije la coordenada X de la proa del Destructor: ")
        while not x.isdigit() or int(x) < 1 or int(x) > n:
            print("Error - Coordenada fuera del cubo")
            x = input("Elije la coordenada X entre 1 y " + str(n) + ": ")
        x = int(x) - 1

        y = input("Elije la coordenada Y de la proa del Destructor: ")
        while not y.isdigit() or int(y) < 1 or int(y) > n:
            print("Error - Coordenada fuera del cubo")
            y = input("Elije la coordenada Y entre 1 y " + str(n) + ": ")
        y = int(y) - 1

        z = input("Elije la coordenada Z de la proa del Destructor: ")
        while not z.isdigit() or int(z) < 1 or int(z) > n:
            print("Error - Coordenada fuera del cubo")
            z = input("Elije la coordenada Z entre 1 y " + str(n) + ": ")
        z = int(z) - 1

        sentido = input("Elige 'vertical' u 'horizontal': ").strip().lower()

        while sentido not in ("vertical", "horizontal"):
            print("Error: ingrese un sentido válido")
            sentido = input("Elige 'vertical' u 'horizontal': ").strip().lower()

        if sentido == "vertical":
            direccion = input("Elige 'arriba' o 'abajo': ").strip().lower()

            while direccion not in ("arriba", "abajo"):
                print("Error: ingrese una dirección válida")
                direccion = input("Elige 'arriba' o 'abajo': ").strip().lower()

            if direccion == "arriba":
                celdas = [
                    (z, y, x),
                    (z, y - 1, x),
                    (z, y - 2, x)
                ]
            else:
                celdas = [
                    (z, y, x),
                    (z, y + 1, x),
                    (z, y + 2, x)
                ]

        else:
            direccion = input(
                "Elige 'derecha', 'izquierda', 'atras' o 'adelante': "
            ).strip().lower()

            while direccion not in ("derecha", "izquierda", "atras", "adelante"):
                print("Error: ingrese una dirección válida")
                direccion = input(
                    "Elige 'derecha', 'izquierda', 'atras' o 'adelante': "
                ).strip().lower()

            if direccion == "derecha":
                celdas = [
                    (z, y, x),
                    (z, y, x + 1),
                    (z, y, x + 2)
                ]
            elif direccion == "izquierda":
                celdas = [
                    (z, y, x),
                    (z, y, x - 1),
                    (z, y, x - 2)
                ]
            elif direccion == "atras":
                celdas = [
                    (z, y, x),
                    (z + 1, y, x),
                    (z + 2, y, x)
                ]
            else:
                celdas = [
                    (z, y, x),
                    (z - 1, y, x),
                    (z - 2, y, x)
                ]

        if posicion_valida(cubo, celdas):
            for z_celda, y_celda, x_celda in celdas:
                cubo[z_celda][y_celda][x_celda] = "?"
            return cubo

        print("Error: el destructor sale del cubo, ocupa una casilla ocupada o toca otra nave.")
        print("Intenta colocar el destructor nuevamente.")


#############################################################################################################


def colocar_submarino(cubo):
    """
    Recibe el cubo y solicita la posición de un submarino.
    Devuelve el cubo con el submarino ubicado.
    """

    n = len(cubo)
    mitad = n // 2

    while True:
        x = input("Elije la coordenada X de la proa del Submarino: ")
        while not x.isdigit() or int(x) < 1 or int(x) > n:
            print("Error - Coordenada fuera del cubo")
            x = input("Elije la coordenada X entre 1 y " + str(n) + ": ")
        x = int(x) - 1

        y = input("Elije la coordenada Y de la proa del Submarino: ")
        while not y.isdigit() or int(y) < 1 or int(y) > n:
            print("Error - Coordenada fuera del cubo")
            y = input("Elije la coordenada Y entre 1 y " + str(n) + ": ")
        y = int(y) - 1

        z = input(
            "Elije la coordenada Z entre " + str(mitad + 1) +
            " y " + str(n) + ": "
        )
        while not z.isdigit() or int(z) < mitad + 1 or int(z) > n:
            print("Error - El submarino debe estar en la mitad inferior del cubo")
            z = input(
                "Elije la coordenada Z entre " + str(mitad + 1) +
                " y " + str(n) + ": "
            )
        z = int(z) - 1

        sentido = input("Elige 'vertical' u 'horizontal': ").strip().lower()

        while sentido not in ("vertical", "horizontal"):
            print("Error: ingrese un sentido válido")
            sentido = input("Elige 'vertical' u 'horizontal': ").strip().lower()

        if sentido == "vertical":
            direccion = input("Elige 'arriba' o 'abajo': ").strip().lower()

            while direccion not in ("arriba", "abajo"):
                print("Error: ingrese una dirección válida")
                direccion = input("Elige 'arriba' o 'abajo': ").strip().lower()

            if direccion == "arriba":
                celdas = [
                    (z, y, x),
                    (z, y - 1, x),
                    (z, y - 2, x)
                ]
            else:
                celdas = [
                    (z, y, x),
                    (z, y + 1, x),
                    (z, y + 2, x)
                ]

        else:
            direccion = input(
                "Elige 'derecha', 'izquierda', 'atras' o 'adelante': "
            ).strip().lower()

            while direccion not in ("derecha", "izquierda", "atras", "adelante"):
                print("Error: ingrese una dirección válida")
                direccion = input(
                    "Elige 'derecha', 'izquierda', 'atras' o 'adelante': "
                ).strip().lower()

            if direccion == "derecha":
                celdas = [
                    (z, y, x),
                    (z, y, x + 1),
                    (z, y, x + 2)
                ]
            elif direccion == "izquierda":
                celdas = [
                    (z, y, x),
                    (z, y, x - 1),
                    (z, y, x - 2)
                ]
            elif direccion == "atras":
                celdas = [
                    (z, y, x),
                    (z + 1, y, x),
                    (z + 2, y, x)
                ]
            else:
                celdas = [
                    (z, y, x),
                    (z - 1, y, x),
                    (z - 2, y, x)
                ]

        mitad_inferior = True

        for z_celda, y_celda, x_celda in celdas:
            if z_celda < mitad:
                mitad_inferior = False

        if mitad_inferior and posicion_valida(cubo, celdas):
            for z_celda, y_celda, x_celda in celdas:
                cubo[z_celda][y_celda][x_celda] = "?"
            return cubo

        print(
            "Error: el submarino sale del cubo, ocupa una casilla ocupada, "
            "toca otra nave o sale de la mitad inferior."
        )
        print("Intenta colocar el submarino nuevamente.")

############################################################################################################


def colocar_crucero(cubo):
    """
    Recibe el cubo y solicita la posición del crucero.
    Devuelve el cubo con el crucero ubicado.
    El crucero ocupa 4 celdas y no puede estar en los extremos de Z.
    """

    n = len(cubo)

    while True:
        x = input("Elije la coordenada X de la proa del Crucero: ")
        while not x.isdigit() or int(x) < 1 or int(x) > n:
            print("Error - Coordenada fuera del cubo")
            x = input("Elije la coordenada X entre 1 y " + str(n) + ": ")
        x = int(x) - 1

        y = input("Elije la coordenada Y de la proa del Crucero: ")
        while not y.isdigit() or int(y) < 1 or int(y) > n:
            print("Error - Coordenada fuera del cubo")
            y = input("Elije la coordenada Y entre 1 y " + str(n) + ": ")
        y = int(y) - 1

        z = input("Elije la coordenada Z entre 2 y " + str(n - 1) + ": ")
        while not z.isdigit() or int(z) < 2 or int(z) > n - 1:
            print("Error - El crucero no puede ocupar los extremos de Z")
            z = input("Elije la coordenada Z entre 2 y " + str(n - 1) + ": ")
        z = int(z) - 1

        sentido = input("Elige 'vertical' u 'horizontal': ").lower()

        while sentido != "vertical" and sentido != "horizontal":
            print("Error: ingrese un sentido válido")
            sentido = input("Elige 'vertical' u 'horizontal': ").lower()

        if sentido == "vertical":
            direccion = input("Elige 'arriba' o 'abajo': ").lower()

            while direccion != "arriba" and direccion != "abajo":
                print("Error: ingrese una dirección válida")
                direccion = input("Elige 'arriba' o 'abajo': ").lower()

            if direccion == "arriba":
                celdas = [
                    (z, y, x),
                    (z, y - 1, x),
                    (z, y - 2, x),
                    (z, y - 3, x)
                ]
            else:
                celdas = [
                    (z, y, x),
                    (z, y + 1, x),
                    (z, y + 2, x),
                    (z, y + 3, x)
                ]

        else:
            direccion = input(
                "Elige 'derecha', 'izquierda', 'atras' o 'adelante': "
            ).lower()

            while direccion not in ("derecha", "izquierda", "atras", "adelante"):
                print("Error: ingrese una dirección válida")
                direccion = input(
                    "Elige 'derecha', 'izquierda', 'atras' o 'adelante': "
                ).lower()

            if direccion == "derecha":
                celdas = [
                    (z, y, x),
                    (z, y, x + 1),
                    (z, y, x + 2),
                    (z, y, x + 3)
                ]
            elif direccion == "izquierda":
                celdas = [
                    (z, y, x),
                    (z, y, x - 1),
                    (z, y, x - 2),
                    (z, y, x - 3)
                ]
            elif direccion == "atras":
                celdas = [
                    (z, y, x),
                    (z + 1, y, x),
                    (z + 2, y, x),
                    (z + 3, y, x)
                ]
            else:
                celdas = [
                    (z, y, x),
                    (z - 1, y, x),
                    (z - 2, y, x),
                    (z - 3, y, x)
                ]

        celdas_validas = True

        for z_celda, y_celda, x_celda in celdas:
            if z_celda < 0 or z_celda >= n:
                celdas_validas = False
            elif y_celda < 0 or y_celda >= n:
                celdas_validas = False
            elif x_celda < 0 or x_celda >= n:
                celdas_validas = False
            elif z_celda == 0 or z_celda == n - 1:
                celdas_validas = False

        if celdas_validas and posicion_valida(cubo, celdas):
            for z_celda, y_celda, x_celda in celdas:
                cubo[z_celda][y_celda][x_celda] = "?"

            return cubo

        print("Error: la posición no es válida.")
        print("El crucero sale del cubo, ocupa una celda ocupada o toca otra nave.")
        print("Intenta ubicarlo nuevamente.")

###################################################################

def colocar_portaaviones(cubo):
    """
    Recibe el cubo y solicita la posición del portaaviones.
    Devuelve el cubo con el portaaviones ubicado.
    El portaaviones ocupa 5 celdas en la mitad superior de Z.
    """

    n = len(cubo)
    mitad = n // 2

    while True:
        x = input("Elije la coordenada X de la proa del Portaaviones: ")
        while not x.isdigit() or int(x) < 1 or int(x) > n:
            print("Error - Coordenada fuera del cubo")
            x = input("Elije X entre 1 y " + str(n) + ": ")
        x = int(x) - 1

        y = input("Elije la coordenada Y de la proa del Portaaviones: ")
        while not y.isdigit() or int(y) < 1 or int(y) > n:
            print("Error - Coordenada fuera del cubo")
            y = input("Elije Y entre 1 y " + str(n) + ": ")
        y = int(y) - 1

        z = input(
            "Elije la coordenada Z entre 1 y " + str(mitad) + ": "
        )
        while not z.isdigit() or int(z) < 1 or int(z) > mitad:
            print("Error - El portaaviones debe estar en la mitad superior de Z")
            z = input(
                "Elije Z entre 1 y " + str(mitad) + ": "
            )
        z = int(z) - 1

        sentido = input("Elige 'vertical' u 'horizontal': ").strip().lower()

        while sentido not in ("vertical", "horizontal"):
            print("Error: ingrese un sentido válido")
            sentido = input("Elige 'vertical' u 'horizontal': ").strip().lower()

        if sentido == "vertical":
            direccion = input("Elige 'arriba' o 'abajo': ").strip().lower()

            while direccion not in ("arriba", "abajo"):
                print("Error: ingrese una dirección válida")
                direccion = input("Elige 'arriba' o 'abajo': ").strip().lower()

            if direccion == "arriba":
                celdas = [
                    (z, y, x), (z, y - 1, x), (z, y - 2, x),
                    (z, y - 3, x), (z, y - 4, x)
                ]
            else:
                celdas = [
                    (z, y, x), (z, y + 1, x), (z, y + 2, x),
                    (z, y + 3, x), (z, y + 4, x)
                ]

        else:
            direccion = input(
                "Elige 'derecha', 'izquierda', 'atras' o 'adelante': "
            ).strip().lower()

            while direccion not in ("derecha", "izquierda", "atras", "adelante"):
                print("Error: ingrese una dirección válida")
                direccion = input(
                    "Elige 'derecha', 'izquierda', 'atras' o 'adelante': "
                ).strip().lower()

            if direccion == "derecha":
                celdas = [
                    (z, y, x), (z, y, x + 1), (z, y, x + 2),
                    (z, y, x + 3), (z, y, x + 4)
                ]
            elif direccion == "izquierda":
                celdas = [
                    (z, y, x), (z, y, x - 1), (z, y, x - 2),
                    (z, y, x - 3), (z, y, x - 4)
                ]
            elif direccion == "atras":
                celdas = [
                    (z, y, x), (z + 1, y, x), (z + 2, y, x),
                    (z + 3, y, x), (z + 4, y, x)
                ]
            else:
                celdas = [
                    (z, y, x), (z - 1, y, x), (z - 2, y, x),
                    (z - 3, y, x), (z - 4, y, x)
                ]

        mitad_superior = True

        for z_celda, y_celda, x_celda in celdas:
            if z_celda < 0 or z_celda >= mitad:
                mitad_superior = False

        if mitad_superior and posicion_valida(cubo, celdas):
            for z_celda, y_celda, x_celda in celdas:
                cubo[z_celda][y_celda][x_celda] = "?"
            return cubo

        print("Error: la posición no es válida.")
        print("Verifica los límites, la mitad superior de Z y la separación entre naves.")

###############################################################################################

def colocar_estacion(cubo):
    """
    Recibe el cubo y solicita la posición de la estación espacial.
    Devuelve el cubo con la estación ubicada.
    La estación ocupa 8 celdas y no puede tocar los bordes.
    """

    n = len(cubo)

    while True:
        print("Selecciona la posición de la estación espacial (2x2x2).")

        x = input("Elije la coordenada X: ")
        while not x.isdigit() or int(x) < 2 or int(x) > n - 2:
            print("Error: la nave no puede ocupar los bordes del cubo.")
            x = input("Elije X entre 2 y " + str(n - 2) + ": ")
        x = int(x) - 1

        y = input("Elije la coordenada Y: ")
        while not y.isdigit() or int(y) < 2 or int(y) > n - 2:
            print("Error: la nave no puede ocupar los bordes del cubo.")
            y = input("Elije Y entre 2 y " + str(n - 2) + ": ")
        y = int(y) - 1

        z = input("Elije la coordenada Z: ")
        while not z.isdigit() or int(z) < 2 or int(z) > n - 2:
            print("Error: la nave no puede ocupar los bordes del cubo.")
            z = input("Elije Z entre 2 y " + str(n - 2) + ": ")
        z = int(z) - 1

        celdas = [
            (z, y, x),
            (z + 1, y, x),
            (z, y, x + 1),
            (z + 1, y, x + 1),
            (z, y + 1, x),
            (z + 1, y + 1, x),
            (z, y + 1, x + 1),
            (z + 1, y + 1, x + 1)
        ]

        if posicion_valida(cubo, celdas):
            for z_celda, y_celda, x_celda in celdas:
                cubo[z_celda][y_celda][x_celda] = "?"
            return cubo

        print("Error: la estación ocupa una posición no válida.")
        print("Puede estar ocupada o tocar otra nave.")
        print("Intenta ubicarla nuevamente.")

#La siguiente función utiliza la lista "celdas" utilizada en la sección de Armamento
#Dicha lista esta formasda por tuplas que contienen las coordenadas de las celdas afectadas por las diferentes armas.
#La siguiente funcion recorre dicha lusta comparando las coordenadas del blanco con las ocupadas.

def verificar_impactos(cubo, celdas):
    for i in range(len(celdas)):
        punto = celdas[i]
        z = punto[0]
        y = punto[1]
        x = punto[2]

        if z < 0 or z >= len(cubo) or \
           y < 0 or y >= len(cubo) or \
           x < 0 or x >= len(cubo):
            continue

        if cubo[z][y][x] == "?":
            cubo[z][y][x] = "I"
            print("Impacto")

        elif cubo[z][y][x] == "~":
            cubo[z][y][x] = "A"
            print("Agua")

        else:
            print("Esta casilla ya fue impactada o no contiene una nave.")

    return cubo
#"derecha" and cubo[z][y][x+4] == "?"
#"izquierda" and cubo[z][y][x-1] == "?"
#"atras" and cubo[z+4][y][x] == "?") or \
#"adelante" and cubo[z-1][y][x] == "?")
#"arriba" and cubo[z][y-2][x] == "?") or \
#"abajo" and cubo[z][y+1][x] == "?")

###############################################################################################

def ubicacion_automatica(cubo, catalogo, semilla=None):
    """
    Ubica automáticamente las naves en el cubo.

    Recibe:
        cubo: cubo donde se ubican las naves.
        catalogo: diccionario con los tipos y cantidades de naves.
        semilla: número para repetir las mismas ubicaciones.

    Devuelve:
        Una lista con los datos de las naves ubicadas.

    Excepciones:
        RuntimeError si no se encuentra una posición válida.
    """

    generador = random.Random(semilla)
    catalogo_ordenado = sorted(
        catalogo.items(),
        key=lambda elemento: elemento[1]["tamanio"],
        reverse=True
    )
    n = len(cubo)
    flota = []

    for nombre, datos in catalogo_ordenado:
        tamanio = datos["tamanio"]
        cantidad = datos["cantidad"]

        for numero in range(cantidad):
            ubicada = False

            intentos = 0

            while not ubicada and intentos < 1000:
                intentos += 1

                if nombre == "Submarino":
                    z = generador.randint(n // 2, n - 1)
                elif nombre == "Portaaviones":
                    z = generador.randint(0, n // 2 - 1)
                elif nombre == "Crucero":
                    z = generador.randint(1, n - 2)
                elif nombre == "Estacion":
                    z = generador.randint(1, n - 3)
                else:
                    z = generador.randint(0, n - 1)

                if nombre == "Estacion":
                    y = generador.randint(1, n - 3)
                    x = generador.randint(1, n - 3)

                    celdas = []

                    for cambio_z in range(2):
                        for cambio_y in range(2):
                            for cambio_x in range(2):
                                celdas.append((
                                    z + cambio_z,
                                    y + cambio_y,
                                    x + cambio_x
                                ))

                else:
                    y = generador.randint(0, n - 1)
                    x = generador.randint(0, n - 1)

                    eje = generador.choice(["x", "y", "z"])
                    direccion = generador.choice([-1, 1])

                    celdas = []

                    for i in range(tamanio):
                        nueva_z = z
                        nueva_y = y
                        nueva_x = x

                        if eje == "x":
                            nueva_x = x + i * direccion
                        elif eje == "y":
                            nueva_y = y + i * direccion
                        else:
                            nueva_z = z + i * direccion

                        celdas.append((
                            nueva_z,
                            nueva_y,
                            nueva_x
                        ))

                reglas_validas = True

                for z_celda, y_celda, x_celda in celdas:
                    if nombre == "Submarino":
                        if z_celda < n // 2:
                            reglas_validas = False

                    elif nombre == "Portaaviones":
                        if z_celda >= n // 2:
                            reglas_validas = False

                    elif nombre == "Crucero":
                        if z_celda == 0 or z_celda == n - 1:
                            reglas_validas = False

                    elif nombre == "Estacion":
                        if (z_celda == 0 or z_celda == n - 1
                                or y_celda == 0 or y_celda == n - 1
                                or x_celda == 0 or x_celda == n - 1):
                            reglas_validas = False

                if reglas_validas and posicion_valida(cubo, celdas):
                    for z_celda, y_celda, x_celda in celdas:
                        cubo[z_celda][y_celda][x_celda] = "?"

                    celdas_partida = []

                    for z_celda, y_celda, x_celda in celdas:
                        celdas_partida.append((
                            z_celda + 1,
                            x_celda + 1,
                            y_celda + 1
                        ))

                    nave = {
                        "nombre": nombre,
                        "celdas": celdas_partida,
                        "impactos": set(),
                        "hundida": False,
                        "resistencia": tamanio
                    }

                    flota.append(nave)
                    ubicada = True

            if not ubicada:
                raise RuntimeError(
                    "No se pudo ubicar la nave: " + nombre
                )

    return flota
def posicion_valida(cubo, celdas):
    """
    Recibe el cubo y una lista de coordenadas de la nave.
    Devuelve True si las celdas están libres y no tocan otras naves.
    """

    n = len(cubo)

    for z, y, x in celdas:

        if z < 0 or z >= n or y < 0 or y >= n or x < 0 or x >= n:
            return False

        if cubo[z][y][x] != "~":
            return False

        for vecino_z in range(z - 1, z + 2):
            for vecino_y in range(y - 1, y + 2):
                for vecino_x in range(x - 1, x + 2):

                    if vecino_z >= 0 and vecino_z < n:
                        if vecino_y >= 0 and vecino_y < n:
                            if vecino_x >= 0 and vecino_x < n:

                                if cubo[vecino_z][vecino_y][vecino_x] == "?":
                                    if (vecino_z, vecino_y, vecino_x) not in celdas:
                                        return False

    return True


# Catalogo de naves

CATALOGO_NAVES = {
    "Fragata": {
        "tamanio": 2,
        "cantidad": 3,
        "funcion": colocar_fragata
    },
    "Destructor": {
        "tamanio": 3,
        "cantidad": 2,
        "funcion": colocar_destructor
    },
    "Submarino": {
        "tamanio": 3,
        "cantidad": 2,
        "funcion": colocar_submarino
    },
    "Crucero": {
        "tamanio": 4,
        "cantidad": 1,
        "funcion": colocar_crucero
    },
    "Portaaviones": {
        "tamanio": 5,
        "cantidad": 1,
        "funcion": colocar_portaaviones
    },
    "Estacion": {
        "tamanio": 8,
        "cantidad": 1,
        "funcion": colocar_estacion
    }
}