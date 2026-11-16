
import pytest

from tablero import (
    crear_cubo,
    ErrorTablero,
    PuntoInvalidoError,
    DimensionesError,
    dibujar_plano_z,
    sumar_matrices,
    recorrer_por_capas,
    obtener_vecinos
)


# Pruebas de crear_cubo

def test_crear_cubo():
    cubo = crear_cubo(3)

    assert len(cubo) == 3
    assert len(cubo[0]) == 3
    assert len(cubo[0][0]) == 3


def test_crear_cubo_dimension_minima():
    cubo = crear_cubo(1)

    assert len(cubo) == 1


def test_crear_cubo_dimension_invalida():
    with pytest.raises(ErrorTablero):
        crear_cubo(0)


# Pruebas de dibujar_plano_z

def test_dibujar_plano_z():
    cubo = crear_cubo(3)

    plano = dibujar_plano_z(cubo, 1)

    assert len(plano) > 0


def test_dibujar_plano_z_ultima_capa():
    cubo = crear_cubo(3)

    plano = dibujar_plano_z(cubo, 3)

    assert len(plano) > 0


def test_dibujar_plano_z_invalido():
    cubo = crear_cubo(3)

    with pytest.raises(PuntoInvalidoError):
        dibujar_plano_z(cubo, 0)


# Pruebas de sumar_matrices

def test_sumar_matrices():
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]

    resultado = sumar_matrices(a, b)

    assert resultado == [[6, 8], [10, 12]]


def test_sumar_matrices_distinto_tamano():
    a = [[1, 2], [3, 4]]
    b = [[1, 2, 3]]

    with pytest.raises(DimensionesError):
        sumar_matrices(a, b)


# Pruebas de recorrer_por_capas

def test_recorrer_por_capas():
    cubo = crear_cubo(3)

    recorrido = recorrer_por_capas(cubo)

    assert len(recorrido) == 27
    assert len(set(recorrido)) == 27


def test_recorrer_por_capas_cubo_minimo():
    cubo = crear_cubo(1)

    recorrido = recorrer_por_capas(cubo)

    assert recorrido == [(1, 1, 1)]


# Pruebas de obtener_vecinos

def test_obtener_vecinos_centro():
    cubo = crear_cubo(3)

    vecinos = obtener_vecinos(cubo, (2, 2, 2))

    assert len(vecinos) == 6


def test_obtener_vecinos_esquina():
    cubo = crear_cubo(3)

    vecinos = obtener_vecinos(cubo, (1, 1, 1))

    assert len(vecinos) == 3


def test_obtener_vecinos_punto_invalido():
    cubo = crear_cubo(3)

    with pytest.raises(PuntoInvalidoError):
        obtener_vecinos(cubo, (4, 1, 1))
