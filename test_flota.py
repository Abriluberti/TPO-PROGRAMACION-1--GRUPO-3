import pytest

import flota
import tablero


def test_ubicar_nave_recta():
    cubo = tablero.crear_cubo(8)

    cubo, flota_jugador = flota.ubicar_nave(cubo, [], "F", (1, 1, 1), (1, 1, 2))

    assert len(flota_jugador) == 1
    nave = flota_jugador[0]
    assert nave["letra"] == "F"
    assert nave["celdas"] == {(1, 1, 1), (1, 1, 2)}
    assert nave["impactos"] == set()
    assert nave["hundida"] is False
    assert cubo[0][0][0] == tablero.NAVE_OCULTA
    assert cubo[0][1][0] == tablero.NAVE_OCULTA


def test_contar_ubicadas():
    cubo = tablero.crear_cubo(8)
    flota_jugador = []

    assert flota.contar_ubicadas(flota_jugador, "F") == 0

    cubo, flota_jugador = flota.ubicar_nave(cubo, flota_jugador, "F", (1, 1, 1), (1, 1, 2))
    assert flota.contar_ubicadas(flota_jugador, "F") == 1
    assert flota.contar_ubicadas(flota_jugador, "D") == 0

    cubo, flota_jugador = flota.ubicar_nave(cubo, flota_jugador, "F", (3, 1, 1), (3, 1, 2))
    assert flota.contar_ubicadas(flota_jugador, "F") == 2


def test_ubicar_nave_no_pisa_la_lista_original():
    """ubicar_nave no debe mutar la lista de flota que recibe."""
    cubo = tablero.crear_cubo(8)
    flota_original = []

    cubo, flota_nueva = flota.ubicar_nave(cubo, flota_original, "F", (1, 1, 1), (1, 1, 2))

    assert flota_original == []
    assert len(flota_nueva) == 1


def test_ubicar_nave_tamanio_incorrecto():
    cubo = tablero.crear_cubo(8)

    with pytest.raises(flota.FlotaError):
        flota.ubicar_nave(cubo, [], "F", (1, 1, 1), (1, 1, 5))


def test_ubicar_nave_no_alineada():
    cubo = tablero.crear_cubo(8)

    with pytest.raises(flota.FlotaError):
        flota.ubicar_nave(cubo, [], "D", (1, 1, 1), (2, 2, 1))


def test_ubicar_nave_respeta_cantidad_maxima():
    cubo = tablero.crear_cubo(8)
    flota_jugador = []

    cubo, flota_jugador = flota.ubicar_nave(cubo, flota_jugador, "F", (1, 1, 1), (1, 1, 2))
    cubo, flota_jugador = flota.ubicar_nave(cubo, flota_jugador, "F", (3, 1, 1), (3, 1, 2))
    cubo, flota_jugador = flota.ubicar_nave(cubo, flota_jugador, "F", (5, 1, 1), (5, 1, 2))

    with pytest.raises(flota.FlotaError):
        flota.ubicar_nave(cubo, flota_jugador, "F", (7, 1, 1), (7, 1, 2))


def test_ubicar_nave_separacion_minima():
    cubo = tablero.crear_cubo(8)
    flota_jugador = []

    cubo, flota_jugador = flota.ubicar_nave(cubo, flota_jugador, "F", (1, 1, 1), (1, 1, 2))

    # pegada (sin celda libre de por medio), debe rechazarse
    with pytest.raises(flota.FlotaError):
        flota.ubicar_nave(cubo, flota_jugador, "D", (1, 2, 1), (1, 2, 3))

    # con una celda libre de por medio, se puede ubicar
    cubo, flota_jugador = flota.ubicar_nave(cubo, flota_jugador, "D", (1, 3, 1), (1, 3, 3))
    assert len(flota_jugador) == 2


def test_submarino_mitad_inferior():
    cubo = tablero.crear_cubo(8)

    with pytest.raises(flota.FlotaError):
        flota.ubicar_nave(cubo, [], "S", (6, 1, 1), (8, 1, 1))

    cubo, flota_jugador = flota.ubicar_nave(cubo, [], "S", (1, 1, 1), (3, 1, 1))
    assert len(flota_jugador) == 1


def test_crucero_no_en_bordes_de_z():
    cubo = tablero.crear_cubo(8)

    with pytest.raises(flota.FlotaError):
        flota.ubicar_nave(cubo, [], "C", (1, 1, 1), (4, 1, 1))

    with pytest.raises(flota.FlotaError):
        flota.ubicar_nave(cubo, [], "C", (5, 1, 1), (8, 1, 1))

    cubo, flota_jugador = flota.ubicar_nave(cubo, [], "C", (2, 1, 1), (5, 1, 1))
    assert len(flota_jugador) == 1


def test_portaaviones_mitad_superior():
    cubo = tablero.crear_cubo(8)

    with pytest.raises(flota.FlotaError):
        flota.ubicar_nave(cubo, [], "P", (1, 1, 1), (5, 1, 1))

    # orientado en el eje x, con z=8 fijo (mitad superior)
    cubo, flota_jugador = flota.ubicar_nave(cubo, [], "P", (8, 1, 1), (8, 5, 1))
    assert len(flota_jugador) == 1


def test_estacion_bloque_2x2x2_no_toca_bordes():
    cubo = tablero.crear_cubo(8)

    # toca el borde z=1: invalido
    with pytest.raises(flota.FlotaError):
        flota.ubicar_nave(cubo, [], "E", (1, 4, 4), (2, 5, 5))

    # bloque interior valido
    cubo, flota_jugador = flota.ubicar_nave(cubo, [], "E", (4, 4, 4), (5, 5, 5))
    nave = flota_jugador[0]
    assert len(nave["celdas"]) == 8


def test_ubicacion_automatica_coloca_toda_la_flota():
    cubo = tablero.crear_cubo(8)

    flota_jugador = flota.ubicacion_automatica(cubo, flota.CATALOGO_NAVES, semilla=123)

    assert len(flota_jugador) == sum(
        datos["cantidad"] for datos in flota.CATALOGO_NAVES.values()
    )

    celdas_totales = [celda for nave in flota_jugador for celda in nave["celdas"]]
    assert len(celdas_totales) == len(set(celdas_totales))  # ninguna nave se superpone


def test_ubicacion_automatica_reproducible_con_semilla():
    cubo_1 = tablero.crear_cubo(8)
    cubo_2 = tablero.crear_cubo(8)

    flota_1 = flota.ubicacion_automatica(cubo_1, flota.CATALOGO_NAVES, semilla=42)
    flota_2 = flota.ubicacion_automatica(cubo_2, flota.CATALOGO_NAVES, semilla=42)

    assert flota_1 == flota_2


def test_ubicacion_automatica_cubo_chico_no_cuelga():
    cubo = tablero.crear_cubo(4)

    with pytest.raises(flota.FlotaError):
        flota.ubicacion_automatica(cubo, flota.CATALOGO_NAVES, semilla=1)


def test_ubicacion_automatica_es_estable_en_cubo_default():
    """Regresion: antes de ubicar primero las naves grandes, esto
    fallaba (FlotaError, casi siempre por la Estacion) hasta 1 de
    cada 10 semillas en un cubo de 8."""
    for semilla in range(100):
        cubo = tablero.crear_cubo(8)
        flota_jugador = flota.ubicacion_automatica(cubo, flota.CATALOGO_NAVES, semilla=semilla)
        assert len(flota_jugador) == sum(
            datos["cantidad"] for datos in flota.CATALOGO_NAVES.values()
        )
