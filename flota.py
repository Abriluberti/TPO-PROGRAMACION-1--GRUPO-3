import random

def colocar_fragata(cubo, tupla_inicio, tupla_final): #2x1

 """Recibe: el cubo, la tupla DESDE y la tupla HASTA.
    Devuelve el cubo con la nave ubicada."""
    a=tupla_inicio[0]-1
    b=tupla_inicio[1]-1
    c=tupla_inicio[2]-1
    
    z=tupla_final[0]-1
    x=tupla_final[1]-1
    y=tupla_final[2]-1
    
    if (a!=z and b!=x) or (a!=z and c!=y) or (b!=x and c!=y):
        raise ValueError("Las celdas no son continuas")
    
    # Si varía en el eje Z (profundidad)
    if b == x and c == y:
        if max(a, z) - min(a, z)!=1:
            raise ValueError("La nave debe ocupar 2 espacios")
        for i in range(min(a, z), max(a, z) + 1):
            if cubo[i][b][c] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for i in range(min(a, z), max(a, z) + 1):
            cubo[i][b][c] = "?"
        print("Fragata colocada")

    # Si varía en el eje X (longitud)
    if a == z and c == y:
        if max(b, x) - min(b, x) !=1:
            raise ValueError("La nave debe ocupar 2 espacios")
        for j in range(min(b, x), max(b, x) + 1):
            if cubo[a][c][j] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for j in range(min(b, x), max(b, x) + 1):
            cubo[a][c][j] = "?"
        print("Fragata colocada")

    # Si varía en el eje Y (altura)
    if a == z and b == x:
        if max(c, y) - min(c, y) !=1:
            raise ValueError("La nave debe ocupar 2 espacios")
        for k in range(min(c, y), max(c, y) + 1):
            if cubo[a][k][b] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for k in range(min(c, y), max(c, y) + 1):
            cubo[a][k][b] = "?"
        print("Fragata colocada")
            
    return cubo

###############################################################################################

def colocar_destructor(cubo, tupla_inicio, tupla_final): #3x1
    """Recibe: el cubo, la tupla DESDE y la tupla HASTA.
        Devuelve el cubo con la nave ubicada."""
    a=tupla_inicio[0]-1
    b=tupla_inicio[1]-1
    c=tupla_inicio[2]-1
    
    z=tupla_final[0]-1
    x=tupla_final[1]-1
    y=tupla_final[2]-1
    
    if (a!=z and b!=x) or (a!=z and c!=y) or (b!=x and c!=y):
        raise ValueError("Las celdas no son continuas")
    
    # Si varía en el eje Z (profundidad)
    if b == x and c == y:
        if max(a, z) - min(a, z)!=2:
            raise ValueError("La nave debe ocupar 3 espacios")
        for i in range(min(a, z), max(a, z) + 1):
            if cubo[i][b][c] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for i in range(min(a, z), max(a, z) + 1):
            cubo[i][b][c] = "?"
        print("Destructor colocado")

    # Si varía en el eje X (longitud)
    if a == z and c == y:
        if max(b, x) - min(b, x)!=2:
            raise ValueError("La nave debe ocupar 3 espacios")
        for j in range(min(b, x), max(b, x) + 1):
            if cubo[a][c][j] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for j in range(min(b, x), max(b, x) + 1):
            cubo[a][c][j] = "?"
        print("Destructor colocado")

    # Si varía en el eje Y (altura)
    if a == z and b == x:
        if max(c, y) - min(c, y) !=2:
            raise ValueError("La nave debe ocupar 3 espacios")
        for k in range(min(c, y), max(c, y) + 1):
            if cubo[a][k][b] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for k in range(min(c, y), max(c, y) + 1):
            cubo[a][k][b] = "?"
        print("Destructor colocado")
            
    return cubo


#############################################################################################################


def colocar_submarino(cubo, tupla_inicio, tupla_final): #3x1 y parte inferior del eje Z
    """Recibe: el cubo, la tupla DESDE y la tupla HASTA.
        Devuelve el cubo con la nave ubicada."""
    a=tupla_inicio[0]-1
    b=tupla_inicio[1]-1
    c=tupla_inicio[2]-1
    
    z=tupla_final[0]-1
    x=tupla_final[1]-1
    y=tupla_final[2]-1
    if c+1<=len(cubo)/2 or y+1<=len(cubo)/2:
        raise ValueError("El submarino no puede colocarse tan alto")
    #Comprueba que el submarino este en la mitad inferior del eje Z.
    
    if (a!=z and b!=x) or (a!=z and c!=y) or (b!=x and c!=y):
        raise ValueError("Las celdas no son continuas")
    #Comprueba que las celdas esten en linea.
    
    # Si varía en el eje Z (profundidad)
    if b == x and c == y:
        if max(a, z) - min(a, z)!=2:
            raise ValueError("La nave debe ocupar 3 espacios")
        for i in range(min(a, z), max(a, z) + 1):
            if cubo[i][b][c] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for i in range(min(a, z), max(a, z) + 1):
            cubo[i][b][c] = "?"
        print("Submarino colocado")

    # Si varía en el eje X (longitud)
    if a == z and c == y:
        if max(b, x) - min(b, x)!=2:
            raise ValueError("La nave debe ocupar 3 espacios")
        for j in range(min(b, x), max(b, x) + 1):
            if cubo[a][c][j] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for j in range(min(b, x), max(b, x) + 1):
            cubo[a][c][j] = "?"
        print("Submarino colocado")

    # Si varía en el eje Y (altura)
    if a == z and b == x:
        if max(c, y) - min(c, y) !=2:
            raise ValueError("La nave debe ocupar 3 espacios")
        for k in range(min(c, y), max(c, y) + 1):
            if cubo[a][k][b] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for k in range(min(c, y), max(c, y) + 1):
            cubo[a][k][b] = "?"
        print("Submarino colocado")
            
    return cubo


############################################################################################################


def colocar_crucero(cubo, tupla_inicio, tupla_final): #4x1 y Z!=1 y Z!=len(cubo)
    """Recibe: el cubo, la tupla DESDE y la tupla HASTA.
        Devuelve el cubo con la nave ubicada."""
    a=tupla_inicio[0]-1
    b=tupla_inicio[1]-1
    c=tupla_inicio[2]-1
    
    z=tupla_final[0]-1
    x=tupla_final[1]-1
    y=tupla_final[2]-1
    if a==0 or z==0 or a==len(cubo)-1 or z==len(cubo)-1:
        raise ValueError("El crucero no puede colocarse en los bordes del eje Z")
    #Verifica que la nave no se encuentre en los bordes del eje Z.
    
    if (a!=z and b!=x) or (a!=z and c!=y) or (b!=x and c!=y):
        raise ValueError("Las celdas no son continuas")
    #Verifica que las celdas esten en linea.
    
    # Si varía en el eje Z (profundidad)
    if b == x and c == y:
        if max(a, z) - min(a, z)!=3:
            raise ValueError("La nave debe ocupar 4 espacios")
        for i in range(min(a, z), max(a, z) + 1):
            if cubo[i][b][c] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for i in range(min(a, z), max(a, z) + 1):
            cubo[i][b][c] = "?"
        print("Crucero colocado")

    # Si varía en el eje X (longitud)
    if a == z and c == y:
        if max(b, x) - min(b, x)!=3:
            raise ValueError("La nave debe ocupar 4 espacios")
        for j in range(min(b, x), max(b, x) + 1):
            if cubo[a][c][j] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for j in range(min(b, x), max(b, x) + 1):
            cubo[a][c][j] = "?"
        print("Crucero colocado")

    # Si varía en el eje Y (altura)
    if a == z and b == x:
        if max(c, y) - min(c, y) !=3:
            raise ValueError("La nave debe ocupar 4 espacios")
        for k in range(min(c, y), max(c, y) + 1):
            if cubo[a][k][b] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for k in range(min(c, y), max(c, y) + 1):
            cubo[a][k][b] = "?"
        print("Crucero colocado")
            
    return cubo

###################################################################

def colocar_portaaviones(cubo, tupla_inicio, tupla_final): #5x1 y parte superior del eje Z
    """Recibe: el cubo, la tupla DESDE y la tupla HASTA.
        Devuelve el cubo con la nave ubicada."""
    a=tupla_inicio[0]-1
    b=tupla_inicio[1]-1
    c=tupla_inicio[2]-1
    
    z=tupla_final[0]-1
    x=tupla_final[1]-1
    y=tupla_final[2]-1
    if c+1>len(cubo)/2 or y+1>len(cubo)/2:
        raise ValueError("El portaaviones no puede colocarse tan bajo")
    #Comprueba que el portaaviones este en la mitad superior del eje Z.
    
    if (a!=z and b!=x) or (a!=z and c!=y) or (b!=x and c!=y):
        raise ValueError("Las celdas no son continuas")
    #Comprueba que las celdas esten en linea.
    
    # Si varía en el eje Z (profundidad)
    if b == x and c == y:
        if max(a, z) - min(a, z)!=4:
            raise ValueError("La nave debe ocupar 5 espacios")
        for i in range(min(a, z), max(a, z) + 1):
            if cubo[i][b][c] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for i in range(min(a, z), max(a, z) + 1):
            cubo[i][b][c] = "?"
        print("Portaaviones colocado")

    # Si varía en el eje X (longitud)
    if a == z and c == y:
        if max(b, x) - min(b, x)!=4:
            raise ValueError("La nave debe ocupar 5 espacios")
        for j in range(min(b, x), max(b, x) + 1):
            if cubo[a][c][j] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for j in range(min(b, x), max(b, x) + 1):
            cubo[a][c][j] = "?"
        print("Portaaviones colocado")

    # Si varía en el eje Y (altura)
    if a == z and b == x:
        if max(c, y) - min(c, y) !=4:
            raise ValueError("La nave debe ocupar 5 espacios")
        for k in range(min(c, y), max(c, y) + 1):
            if cubo[a][k][b] == "?":
                raise ValueError("Ya hay otra nave ocupando esa posición.")
        for k in range(min(c, y), max(c, y) + 1):
            cubo[a][k][b] = "?"
        print("Portaaviones colocado")
            
    return cubo

###############################################################################################

def colocar_estacion(cubo, tupla_inicio, tupla_final): #4x1 y Z!=1 y Z!=len(cubo)
    """Recibe: el cubo, la tupla DESDE y la tupla HASTA. Ambas coordenadas son vertices diagonales opuestos.
        Devuelve el cubo con la estacion ubicada."""
    a=tupla_inicio[0]-1
    b=tupla_inicio[1]-1
    c=tupla_inicio[2]-1
    
    z=tupla_final[0]-1
    x=tupla_final[1]-1
    y=tupla_final[2]-1
    if a==0 or a>=len(cubo) or b==0 or b>=len(cubo) or c==0 or c>=len(cubo) or z==0 or z>=len(cubo) or x==0 or x>=len(cubo) or y==0 or y>=len(cubo):
        raise ValueError("La estacion no puede colocarse en los bordes del cubo")
    #Comprueba que la estacion no se encuentre tocando ningun borde del cubo.
    
    if a==z or b==x or c==y:
        raise ValueError("Las celdas no deben son continuas para la estacion")
    #Verifica que las celdas NO esten en linea.
    else:
        if max(a, z) - min(a, z)!=1 or max(b,x) - min(b, x)!=1 or max(c, y) - min(c, y) !=1:
            raise ValueError("La nave debe ocupar un espacio de 2x2x2")
        elif cubo[a][b][c]=="?" or cubo[a][b][c+1]=="?" or cubo[a][b+1][c]=="?" or cubo[a][b+1][c+1]=="?" or cubo[a+1][b][c]=="?" or cubo[a+1][b][c+1]=="?" or cubo[a+1][b+1][c]=="?" or cubo[a+1][b+1][c+1]=="?":
            raise ValueError("Ya hay otra nave ocupando esa posición.")
        #Verifica que ningun punto del cubo este ocupado al verificar sus 8 celdas.
        else:
            for i in range(min(a,z), max(a,z)+1):
                for j in range(min(c,y), max(c,y)+1):
                    for k in range(min(b,x), max(b,x)+1):
                        cubo[i][j][k] = "?"
            print("Estación colocada")
    return cubo

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