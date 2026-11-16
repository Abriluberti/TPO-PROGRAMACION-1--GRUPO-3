import csv
import json
import os
import re

def estadisticas(historial): 
     """Cuenta las jugadas de cada jugador.

    Recibe: historial (lista de jugadas).
    Devuelve: diccionario {jugador: {"disparos", "impactos", "aguas"}}.
    Lanza: nada.
    """
    resultado = {}
    for accion in historial:
        jugador = accion["jugador"]
        if jugador not in resultado:
            resultado[jugador] = {"disparos": 0, "impactos": 0, "aguas": 0}
        resultado[jugador]["disparos"] += 1
    return resultado 


def resumen_final(historial, ganador):
    """Arma el texto del resumen al terminar la partida.

    Recibe: historial (lista de jugadas) y ganador (str).
    Devuelve: texto (str) para que el integrador lo imprima.
    Lanza: nada.
    """
    resultado = estadisticas(historial)
    texto = " RESUMEN DE LA PARTIDA \n"
    texto += "Turnos jugados: " + str(len(historial)) + "\n"
    texto += "Ganador: " + ganador + "\n"
    for jugador in resultado:
        datos = resultado[jugador]
        texto += jugador + ": " + str(datos["disparos"]) + " disparos, "
        texto += str(datos["impactos"]) + " impactos, "
        texto += str(datos["aguas"]) + " aguas\n"
    return texto

CARPETA_PARTIDAS = os.path.join("datos", "partidas")
CARPETA_EXPORTACIONES = os.path.join("datos", "exportaciones")
RUTA_INDICE = os.path.join("datos", "partidas", "indice.txt")
RUTA_RANKING = os.path.join("datos", "ranking.json")


class RegistroError(Exception):


class PartidaNoEncontradaError(RegistroError):


def validar_nombre(nombre):
    """Revisa que el nombre tenga solo letras, números, - o _.

    Recibe: nombre.
    Devuelve: None.
    Lanza: RegistroError si el nombre no es válido (hasta 30 caracteres).
    """
    if not re.match(r"^[A-Za-z0-9_-]{1,30}$", str(nombre)):
        raise RegistroError("Nombre invalido: solo letras, numeros, - y _.")


def leer_json(ruta, valor_si_no_existe):
    """Lee un archivo JSON.

    Recibe: ruta y valor_si_no_existe (se devuelve si no hay archivo).
    Devuelve: lo que contiene el archivo.
    Lanza: RegistroError si el JSON es inválido o no se puede leer.
    """
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        return valor_si_no_existe
    except json.JSONDecodeError:
        raise RegistroError("El archivo " + ruta + " esta danado.")
    except OSError as e:
        raise RegistroError("No se pudo leer " + ruta + ": " + str(e))
    else:
        return datos


def escribir_json(ruta, datos):
    """Escribe datos en un archivo JSON.

    Recibe: ruta (str) y datos (dict o lista).
    Devuelve: None.
    Lanza: RegistroError si no se puede escribir (por ejemplo, si la
           carpeta no existe o los datos no se pueden guardar).
    """
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
    except (OSError, TypeError) as e:
        raise RegistroError("No se pudo escribir " + ruta + ": " + str(e))


def guardar_partida(estado, nombre):
    """Guarda la partida en datos/partidas/<nombre>.json.

    Recibe: estado (dict) y nombre (str).
    Devuelve: la ruta del archivo escrito.
    Lanza: RegistroError si el nombre es inválido o no se puede guardar.
    """
    validar_nombre(nombre)
    ruta = os.path.join(CARPETA_PARTIDAS, nombre + ".json")
    escribir_json(ruta, estado)

    if nombre not in listar_partidas():
        try:
            with open(RUTA_INDICE, "a", encoding="utf-8") as archivo:
                archivo.write(nombre + "\n")
        except OSError as e:
            raise RegistroError("No se pudo anotar la partida: " + str(e))
    return ruta


def cargar_partida(nombre):
    """Carga una partida guardada.

    Ojo: las tuplas vuelven como listas. Para volver a tener un punto
    (z, x, y) usar lista_a_punto.

    Recibe: nombre.
    Devuelve: el estado de la partida (dict).
    Lanza: RegistroError si el nombre es inválido o el archivo está dañado;
           PartidaNoEncontradaError si la partida no existe.
    """
    validar_nombre(nombre)
    ruta = os.path.join(CARPETA_PARTIDAS, nombre + ".json")
    estado = leer_json(ruta, None)
    if estado is None:
        raise PartidaNoEncontradaError("No existe la partida " + nombre)
    return estado


def lista_a_punto(lista):
    """Convierte una lista [z, x, y] otra vez en el punto (z, x, y).

    Recibe: lista (de 3 números).
    Devuelve: tupla (z, x, y).
    Lanza: nada.
    """
    return tuple(lista)

def listar_partidas():
    """Lista los nombres de las partidas guardadas.

    Lee indice.txt, donde guardar_partida anota un nombre por línea.

    Recibe: nada.
    Devuelve: lista de nombres (str), ordenada. Vacía si no hay ninguna.
    Lanza: RegistroError si no se puede leer el índice.
    """
    nombres = []
    try:
        with open(RUTA_INDICE, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                nombres.append(linea.rstrip("\n"))
    except FileNotFoundError:
        return []
    except OSError as e:
        raise RegistroError("No se pudo leer el indice: " + str(e))
    return sorted(nombres)


def exportar_historial(historial, nombre):
    """Exporta el historial a un archivo CSV en datos/exportaciones/.

    Recibe: historial (lista de jugadas) y nombre (str) del archivo.
    Devuelve: la ruta del CSV (columnas: turno, jugador, arma, objetivo,
              resultado).
    Lanza: RegistroError si el nombre es inválido o no se puede escribir.
    """
    validar_nombre(nombre)
    ruta = os.path.join(CARPETA_EXPORTACIONES, nombre + ".csv")
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo, delimiter=";")
            escritor.writerow(["turno", "jugador", "arma", "objetivo",
                               "resultado"])
            turno = 1
            for accion in historial:
                z, x, y = accion["objetivo"]
                punto = str(z) + "," + str(x) + "," + str(y)
                escritor.writerow([turno, accion["jugador"], accion["arma"],
                                   punto, accion["resultado"]])
                turno += 1
    except OSError as e:
        raise RegistroError("No se pudo exportar: " + str(e))
    return ruta


def actualizar_ranking(jugadores, ganador):
    """Suma una partida jugada a cada jugador y una ganada al ganador.

    Recibe: jugadores (lista de nombres) y ganador (str, o None si nadie
            ganó: en ese caso no se suma nada).
    Devuelve: el ranking: {jugador: {"jugadas": n, "ganadas": n}}.
    Lanza: RegistroError si el ranking está dañado o no se puede guardar.
    """
    ranking = leer_json(RUTA_RANKING, {})
    if ganador is None:
        return ranking
    for jugador in jugadores:
        ranking.setdefault(jugador, {"jugadas": 0, "ganadas": 0})
        ranking[jugador]["jugadas"] += 1
        if jugador == ganador:
            ranking[jugador]["ganadas"] += 1
    escribir_json(RUTA_RANKING, ranking)
    return ranking


def obtener_ranking():
    """Devuelve el ranking ordenado.

    Recibe: nada.
    Devuelve: lista de tuplas (jugador, ganadas, jugadas), de más a menos
              ganadas. Si empatan, va primero el que jugó menos partidas.
    Lanza: RegistroError si el ranking está dañado.
    """
    ranking = leer_json(RUTA_RANKING, {})
    lista = []
    for jugador in ranking:
        ganadas = ranking[jugador]["ganadas"]
        jugadas = ranking[jugador]["jugadas"]
        lista.append((jugador, ganadas, jugadas))
    return sorted(lista, key=lambda t: (-t[1], t[2]))