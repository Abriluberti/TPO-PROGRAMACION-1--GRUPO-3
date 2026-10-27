
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
                estado = cubo[z][x][y]
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
                        estado_vecino = cubo[vz][vx][vy]
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
 
    Este módulo no modifica el cubo: quien llama (armamento.py o el
    integrador) decide si marca los contactos como DETECTADO_SONAR.
 
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
        if cubo[z - 1][x - 1][y - 1] == NAVE_OCULTA:
            contactos.append((z, x, y))
 
    metricas = {
        "comparaciones": comparaciones,
        "profundidad_max": 0,
    }
    return contactos, metricas