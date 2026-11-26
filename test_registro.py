import os

import pytest

import registro
registro.CARPETA_PARTIDAS = os.path.join("datos", "pruebas")
registro.CARPETA_EXPORTACIONES = os.path.join("datos", "pruebas")
registro.RUTA_INDICE = os.path.join("datos", "pruebas", "indice.txt")
registro.RUTA_RANKING = os.path.join("datos", "pruebas", "ranking.json")


def limpiar():
    """Deja vacíos el índice y el ranking de pruebas."""
    with open(registro.RUTA_INDICE, "w", encoding="utf-8") as archivo:
        archivo.write("")
    with open(registro.RUTA_RANKING, "w", encoding="utf-8") as archivo:
        archivo.write("{}")


def historial_de_ejemplo():
    """Historial de 3 jugadas que usan varios tests de este archivo.

    Ana dispara 2 veces (1 impacto, 1 agua) y Luis 1 vez con un
    resultado que no es ni impacto ni agua (ej: tiro invalido), para
    poder distinguir en los asserts que esos dos no se cuentan.
    """
    return [
        {"jugador": "Ana", "arma": "T", "objetivo": (4, 2, 7), "resultado": "impacto"},
        {"jugador": "Luis", "arma": "T", "objetivo": (1, 1, 1), "resultado": "invalido"},
        {"jugador": "Ana", "arma": "T", "objetivo": (5, 5, 5), "resultado": "agua"},
    ]



def test_registro_agrega_las_jugadas():
    historial = historial_de_ejemplo()
    assert len(historial) == 3
    assert historial[0]["jugador"] == "Ana"


def test_estadisticas():
    stats = registro.estadisticas(historial_de_ejemplo())
    assert stats["Ana"] == {"disparos": 2, "impactos": 1, "aguas": 1}
    assert stats["Luis"] == {"disparos": 1, "impactos": 0, "aguas": 0}


def test_resumen_final():
    texto = registro.resumen_final(historial_de_ejemplo(), "Ana")
    assert "Ganador: Ana" in texto
    assert "Ana: 2 disparos, 1 impactos, 1 aguas" in texto


def test_nombre_invalido():
    with pytest.raises(registro.RegistroError):
        registro.validar_nombre("../malo")


def test_guardar_y_cargar():
    limpiar()
    estado = {"turno": 3, "jugadores": ["Ana", "Luis"]}
    registro.guardar_partida(estado, "prueba")
    assert registro.cargar_partida("prueba") == estado


def test_cargar_partida_que_no_existe():
    with pytest.raises(registro.PartidaNoEncontradaError):
        registro.cargar_partida("no_existe_nunca")


def test_listar_partidas():
    limpiar()
    registro.guardar_partida({"a": 1}, "pb")
    registro.guardar_partida({"a": 1}, "pa")
    assert registro.listar_partidas() == ["pa", "pb"]


def test_exportar_historial():
    ruta = registro.exportar_historial(historial_de_ejemplo(), "historial")
    with open(ruta, "r", encoding="utf-8") as archivo:
        lineas = archivo.read().splitlines()
    assert lineas[0] == "turno;jugador;arma;objetivo;resultado"
    assert lineas[1] == "1;Ana;T;4,2,7;impacto"


def test_ranking():
    limpiar()
    registro.actualizar_ranking(["Ana", "Luis"], "Ana")
    registro.actualizar_ranking(["Ana", "Luis"], "Luis")
    registro.actualizar_ranking(["Ana", "Luis"], "Ana")
    assert registro.obtener_ranking() == [("Ana", 2, 3), ("Luis", 1, 3)]
