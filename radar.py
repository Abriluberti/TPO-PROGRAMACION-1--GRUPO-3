

AGUA_SIN_EXPLORAR = "~"
NAVE_OCULTA = "?"
AGUA_MARCADA = "A"
IMPACTO = "I"
HUNDIDO = "#"
DETECTADO_SONAR = "S"

VECINOS_ORTOGONALES = (
    (1, 0, 0), (-1, 0, 0),
    (0, 1, 0), (0, -1, 0),
    (0, 0, 1), (0, 0, -1),
    )

ESTADOS_DE_NAVE = {NAVE_OCULTA, IMPACTO, HUNDIDO}



def buscar_lineal(cubo, estado_buscado=NAVE_OCULTA):
    """Busca en el cubo todas las celdas con un estado dado (método lineal).
 
    Recorre las N*N*N celdas con tres ciclos for anidados, sin estructuras
    auxiliares para decidir: solo se usa una lista donde se acumulan los
    hallazgos.
 
    Recibe:
        cubo: lista de listas de listas (N x N x N), creada por tablero.py.
        estado_buscado: estado de celda a localizar. Por defecto NAVE_OCULTA.
    Devuelve:
        Una tupla (puntos, metricas).
        puntos: lista de tuplas (z, x, y), con valores de 1 a N, en el
            orden en que fueron encontradas.
        metricas: diccionario con las claves "comparaciones" (int),
            "tiempo_ms" (float) y "profundidad_max" (int). El tiempo queda en
            0.0 por ahora. La profundidad vale 0 porque este método no es
            recursivo.
    Lanza:
        No lanza excepciones propias. Si el cubo no es una matriz anidada
        N x N x N, Python puede lanzar TypeError o IndexError.
    """
    n = len(cubo)

    puntos = []
    comparaciones = 0
    for z in range(n):
        for x in range(n):
            for y in range(n):
                comparaciones += 1
                if cubo[z][y][x] == estado_buscado:
                    puntos.append((z + 1, x + 1, y + 1))

    metricas = {
        "comparaciones": comparaciones,
    }
    return puntos, metricas


def buscar_optimizada(cubo, estado_buscado=NAVE_OCULTA):
    """Busca celdas de nave con un estado dado usando paridad y expansión.
 
    Como funciona la busqueda optimizada:
      Toda nave mide al menos 2 celdas contiguas, y dos celdas
      contiguas siempre tienen paridad distinta en z + x + y (una suma
      par y la otra impar). Por lo tanto, toda nave tiene al menos una
      celda con suma par, y alcanza con revisar solo esas celdas: la
      mitad del cubo.

      Al encontrar una celda de nave se recorren sus vecinos
      ortogonales para sacar el resto de la nave. Como entre dos naves
      siempre queda al menos una celda libre, la expansión no se
      "escapa" a otra nave.
      
      Una celda ya revisada no se vuelve a leer.
 
    Se expande por celdas de nave en cualquier estado (oculta, impactada u
    hundida) porque, una vez que una nave recibe impactos, sus celdas
    ocultas pueden quedar separadas por celdas impactadas.
 
    Recibe:
        cubo: lista de listas de listas (N x N x N), creada por tablero.py.
        estado_buscado: NAVE_OCULTA, IMPACTO o HUNDIDO. Por defecto
            NAVE_OCULTA.
    Devuelve:
        Una tupla (puntos, metricas), con el mismo formato y el mismo
        orden que buscar_lineal. La profundidad vale 0 porque no usa
        recursión. Cada lectura del estado de una celda del cubo cuenta
        como una comparación.
    Lanza:
        ValueError: si estado_buscado no es un estado de nave, porque en
            ese caso la estrategia de paridad no es válida.
    """
    if estado_buscado not in ESTADOS_DE_NAVE:
        raise ValueError("buscar_optimizada solo busca celdas de nave.")
 
    n = len(cubo)
 
    puntos = []
    comparaciones = 0
    visitadas = set()
 
    for z in range(n):
        for x in range(n):
            for y in range(n):
                if (z + x + y) % 2 != 0:
                    continue
                if (z, x, y) in visitadas:
                    continue
 
                visitadas.add((z, x, y))
                comparaciones += 1
                estado = cubo[z][y][x]
                if estado not in ESTADOS_DE_NAVE:
                    continue
 
                if estado == estado_buscado:
                    puntos.append((z + 1, x + 1, y + 1))
 
                pendientes = [(z, x, y)]
                while pendientes:
                    pz, px, py = pendientes.pop()
                    for dz, dx, dy in VECINOS_ORTOGONALES:
                        vz, vx, vy = pz + dz, px + dx, py + dy
                        if not (0 <= vz < n and 0 <= vx < n and 0 <= vy < n):
                            continue
                        if (vz, vx, vy) in visitadas:
                            continue
 
                        visitadas.add((vz, vx, vy))
                        comparaciones += 1
                        estado_vecino = cubo[vz][vy][vx]
                        if estado_vecino in ESTADOS_DE_NAVE:
                            if estado_vecino == estado_buscado:
                                puntos.append((vz + 1, vx + 1, vy + 1))
                            pendientes.append((vz, vx, vy))
 
    puntos.sort()
 
    metricas = {
        "comparaciones": comparaciones,
        "profundidad_max": 0,
    }
    return puntos, metricas

def _plano_z(n, valor):
    """Celdas del plano z = valor: recorre todos los x y todos los y."""
    celdas = []
    for x in range(1, n + 1):
        for y in range(1, n + 1):
            celdas.append((valor, x, y))
    return celdas


def _plano_x(n, valor):
    """Celdas del plano x = valor: recorre todos los z y todos los y."""
    celdas = []
    for z in range(1, n + 1):
        for y in range(1, n + 1):
            celdas.append((z, valor, y))
    return celdas


def _plano_y(n, valor):
    """Celdas del plano y = valor: recorre todos los z y todos los x."""
    celdas = []
    for z in range(1, n + 1):
        for x in range(1, n + 1):
            celdas.append((z, x, valor))
    return celdas

PLANOS = {
    "z": _plano_z,
    "x": _plano_x,
    "y": _plano_y,
}

def sonar_plano(cubo, eje, valor):
    """Revela un plano entero del cubo y devuelve los contactos con naves.
 
    Recibe:
        cubo: lista de listas de listas (N x N x N), creada por tablero.py.
        eje: "z", "x" o "y".
        valor: número de 1 a N del plano elegido.
    Devuelve:
        Una tupla (contactos, metricas).
        contactos: lista de tuplas (z, x, y), con valores de 1 a N.
        metricas: diccionario con "comparaciones" (siempre N*N),
            "tiempo_ms" y "profundidad_max" (0).
    Lanza:
        ValueError: si el eje no es "z", "x" o "y", o si el valor está
            fuera del rango 1 a N.
    """
    n = len(cubo)
 
    if eje not in PLANOS:
        raise ValueError("El eje debe ser z, x o y.")
    if not 1 <= valor <= n:
        raise ValueError("El valor del plano debe estar entre 1 y N.")
 
    celdas = PLANOS[eje](n, valor)
 
    contactos = []
    comparaciones = 0
    for z, x, y in celdas:
        comparaciones += 1
        if cubo[z - 1][y - 1][x - 1] == NAVE_OCULTA:
            contactos.append((z, x, y))
 
    metricas = {
        "comparaciones": comparaciones,
        "profundidad_max": 0,
    }
    return contactos, metricas

def buscar_recursiva(cubo, estado_buscado=NAVE_OCULTA, z=0):
    """Busca en el cubo todas las celdas con un estado dado en forma recursiva.

    Recorre el cubo capa por capa sobre el eje z llamándose a sí misma
    con z + 1 hasta llegar al final del cubo.

    Recibe:
        cubo: lista de listas de listas (N x N x N), creada por tablero.py.
        estado_buscado: estado de celda a localizar. Por defecto NAVE_OCULTA.
        z: índice de la capa actual (por defecto 0 para empezar desde el inicio).
    Devuelve:
        Una tupla (puntos, metricas).
        puntos: lista de tuplas (z, x, y), con valores de 1 a N.
        metricas: diccionario con "comparaciones" (int) y "profundidad_max" (int).
    """
    n = len(cubo)

    #1. CASO BASE
    if z == n:
        return [], {"comparaciones": 0, "profundidad_max": 0}

    puntos_esta_capa = []
    comparaciones_esta_capa = 0

    for x in range(n):
        for y in range(n):
            comparaciones_esta_capa += 1
            if cubo[z][y][x] == estado_buscado:
                puntos_esta_capa.append((z + 1, x + 1, y + 1))

    # 3. PASO RECURSIVO
    puntos_siguientes, metricas_siguientes = buscar_recursiva(
        cubo, estado_buscado, z + 1
    )

    # 4. se juntan los resultados de esta capa con los de las capas siguientes
    puntos_totales = puntos_esta_capa + puntos_siguientes
    metricas_totales = {
        "comparaciones": comparaciones_esta_capa + metricas_siguientes["comparaciones"],
        "profundidad_max": metricas_siguientes["profundidad_max"] + 1,
    }

    return puntos_totales, metricas_totales

def recorrer_por_capas(cubo, origen=None):
    """Recorre el cubo de forma iterativa desde la capa z = 1 hasta z = N.

    Recibe:
        cubo: lista de listas de listas (N x N x N).
        origen: parámetro opcional (no se usa, mantiene la misma firma).
    Devuelve:
        Lista de tuplas (z, x, y) en orden de capa 1 a N.
    """
    n = len(cubo)
    recorrido = []

    for z in range(1, n + 1):
        for x in range(1, n + 1):
            for y in range(1, n + 1):
                recorrido.append((z, x, y))

    return recorrido


def recorrer_capas_inverso(cubo, origen=None, z=1):
    """Recorre el cubo en forma recursiva desde el fondo (z = N) hacia z = 1.

    Recibe:
        cubo: lista de listas de listas (N x N x N).
        origen: parámetro opcional para compatibilidad con el diccionario.
        z: número de capa actual (inicia en 1 por defecto).
    Devuelve:
        Lista de tuplas (z, x, y) desde la última capa hasta la primera.
    """
    n = len(cubo)

    # 1. CASO BASE
    if z > n:
        return []

    # 2. Armar la lista de puntos de la capa z actual
    puntos_esta_capa = []
    for x in range(1, n + 1):
        for y in range(1, n + 1):
            puntos_esta_capa.append((z, x, y))

    # 3. PASO RECURSIVO
    # y se le suma la capa actual al final para que quede invertido (de N a 1)
    capas_inferiores = recorrer_capas_inverso(cubo, origen, z + 1)
    return capas_inferiores + puntos_esta_capa


def recorrer_propagacion(cubo, origen=(1, 1, 1), radio=2, visitadas=None):
    """Recorre el cubo propagando en forma recursiva desde un punto hacia sus vecinos.

    Recibe:
        cubo: lista de listas de listas (N x N x N).
        origen: tupla (z, x, y) desde donde inicia la expansión (de 1 a N).
        radio: cantidad de pasos que se expande hacia los vecinos.
        visitadas: lista donde se acumulan los puntos recorridos sin repetir.
    Devuelve:
        Lista de tuplas (z, x, y) visitadas durante la propagación.
    Lanza ValueError si el punto de origen inicial está fuera del cubo.
    """
    n = len(cubo)
    if origen is None:
        origen = (1, 1, 1)

    z, x, y = origen

    if visitadas is None:
        if not (1 <= z <= n and 1 <= x <= n and 1 <= y <= n):
            raise ValueError("El punto de origen está fuera del cubo.")
        visitadas = []

    # 1. CASO BASE
    if not (1 <= z <= n and 1 <= x <= n and 1 <= y <= n):
        return visitadas

    if origen not in visitadas:
        visitadas.append(origen)

    # 3. CASO BASE DE RADIO: si se agotan los pasos de expansión, se detiene la funcion
    if radio <= 0:
        return visitadas

    # 4. PASO RECURSIVO
    for dz, dx, dy in VECINOS_ORTOGONALES:
        vecino = (z + dz, x + dx, y + dy)
        if vecino not in visitadas:
            recorrer_propagacion(cubo, vecino, radio - 1, visitadas)

    return visitadas

RECORRIDOS = {
    "capas": recorrer_por_capas,
    "inverso": recorrer_capas_inverso,
    "propagacion": recorrer_propagacion,
}


def ejecutar_recorrido(nombre, cubo, origen=None):
    """Selecciona y ejecuta un recorrido del cubo mediante el diccionario RECORRIDOS.

    Recibe:
        nombre: "capas", "inverso" o "propagacion".
        cubo: lista de listas de listas (N x N x N).
        origen: tupla (z, x, y) opcional para el recorrido por propagación.
    Devuelve:
        Lista de tuplas (z, x, y) en el orden recorrido.
    Lanza ValueError si el nombre del recorrido no existe en RECORRIDOS.
    """
    if nombre not in RECORRIDOS:
        raise ValueError("El recorrido debe ser 'capas', 'inverso' o 'propagacion'.")

    funcion_recorrido = RECORRIDOS[nombre]
    return funcion_recorrido(cubo, origen)

def mapa_probabilidad(cubo):
    """Calcula un cubo N x N x N con el puntaje de probabilidad de cada celda.

    Evalúa cada celda sin revelar las naves ocultas ("?"):
      - Si la celda ya fue atacada (AGUA_MARCADA, IMPACTO o HUNDIDO), vale 0.
      - Si está sin atacar, suma +1 por cada vecino ortogonal disponible y
        +20 por cada vecino que tenga un IMPACTO previo.
      - Si fue marcada como DETECTADO_SONAR, suma +50 de prioridad.

    Recibe:
        cubo: lista de listas de listas (N x N x N), creada por tablero.py.
    Devuelve:
        Matriz anidada N x N x N de enteros con el puntaje de cada celda,
        indexada igual que el cubo (mapa[z][y][x]).
    Lanza:
        No lanza excepciones propias.
    """
    n = len(cubo)

    mapa = []
    for z in range(n):
        capa = []
        for y in range(n):
            fila = []
            for x in range(n):
                fila.append(0)
            capa.append(fila)
        mapa.append(capa)

    for z in range(n):
        for x in range(n):
            for y in range(n):
                estado = cubo[z][y][x]

                
                if estado in (AGUA_MARCADA, IMPACTO, HUNDIDO):
                    mapa[z][y][x] = 0
                    continue

                puntaje = 0

                
                if estado == DETECTADO_SONAR:
                    puntaje += 50

                
                for dz, dx, dy in VECINOS_ORTOGONALES:
                    vz, vx, vy = z + dz, x + dx, y + dy

                    if 0 <= vz < n and 0 <= vx < n and 0 <= vy < n:
                        estado_vecino = cubo[vz][vy][vx]

                        
                        if estado_vecino not in (AGUA_MARCADA, HUNDIDO):
                            puntaje += 1

                        
                        if estado_vecino == IMPACTO:
                            puntaje += 20

                mapa[z][y][x] = puntaje

    return mapa