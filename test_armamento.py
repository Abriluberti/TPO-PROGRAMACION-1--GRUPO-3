
import pytest
import armamento
import tablero


def test_validar_punto():
    assert armamento._validar_punto((1, 2, 3), 5)
    assert not armamento._validar_punto((0, 2, 3), 5)
    assert not armamento._validar_punto((6, 2, 3), 5)
    assert not armamento._validar_punto((1, 2), 5)


def test_torpedo():
    cubo = tablero.crear_cubo(5)

    resultado = armamento.torpedo(cubo, (2, 3, 4))

    assert resultado == {(2, 3, 4)}


def test_racimo():
    cubo = tablero.crear_cubo(5)

    resultado = armamento.racimo(cubo, (3, 3, 3))

    assert len(resultado) == 7
    assert (3, 3, 3) in resultado


def test_carga_profundidad():
    cubo = tablero.crear_cubo(5)

    resultado = armamento.carga_profundidad(cubo, (2, 3, 4))

    esperadas = {(z, 3, 4) for z in range(1, 6)}

    assert resultado == esperadas


def test_barrido_laser_x():
    cubo = tablero.crear_cubo(5)

    resultado = armamento.barrido_laser(cubo, (2, 3, 4), "x")

    esperadas = {(2, x, 4) for x in range(1, 6)}

    assert resultado == esperadas


def test_barrido_laser_y():
    cubo = tablero.crear_cubo(5)

    resultado = armamento.barrido_laser(cubo, (2, 3, 4), "y")

    esperadas = {(2, 3, y) for y in range(1, 6)}

    assert resultado == esperadas


def test_barrido_laser_eje_invalido():
    cubo = tablero.crear_cubo(5)

    resultado = armamento.barrido_laser(cubo, (2, 3, 4), "z")

    assert resultado == set()


def test_onda_expansiva():
    cubo = tablero.crear_cubo(5)

    resultado = armamento.onda_expansiva(
        cubo, (3, 3, 3), radio=1
    )

    assert len(resultado) == 7
    assert (3, 3, 3) in resultado


def test_onda_expansiva_radio_cero():
    cubo = tablero.crear_cubo(5)

    resultado = armamento.onda_expansiva(
        cubo, (3, 3, 3), radio=0
    )

    assert resultado == {(3, 3, 3)}


def test_onda_expansiva_radio_invalido():
    cubo = tablero.crear_cubo(5)

    resultado = armamento.onda_expansiva(
        cubo, (3, 3, 3), radio=-1
    )

    assert resultado == set()


def test_torpedo_guiado():
    cubo = tablero.crear_cubo(5)

    nave = {
        "celdas": [(2, 2, 2), (2, 3, 2), (2, 4, 2)],
        "impactos": {(2, 2, 2)},
        "hundida": False
    }

    resultado = armamento.torpedo_guiado(
        cubo, (2, 2, 2), flota=[nave]
    )

    assert resultado == {(2, 3, 2)}


def test_torpedo_guiado_sin_impacto():
    cubo = tablero.crear_cubo(5)

    resultado = armamento.torpedo_guiado(
        cubo, (2, 2, 2), flota=[]
    )

    assert resultado == set()



def test_municion_inicial():
    municion = armamento.municion_inicial()

    assert municion["T"] is None
    assert municion["R"] == 3
    assert municion["C"] == 2
    assert municion["S"] == 4
    assert municion["L"] == 2
    assert municion["O"] == 1
    assert municion["G"] == 1

def test_gastar_municion():
    municion = armamento.municion_inicial()

    armamento.gastar_municion("R", municion)

    assert municion["R"] == 2


def test_municion_torpedo_ilimitada():
    municion = armamento.municion_inicial()

    armamento.gastar_municion("T", municion)

    assert municion["T"] is None


def test_aplicar_disparo():
    cubo = tablero.crear_cubo(5)
    municion = armamento.municion_inicial()

    ocupadas = {(2, 3, 3)}

    resultado = armamento.aplicar_disparo(
        "T", cubo, (2, 3, 3), ocupadas, municion
    )

    assert resultado["impactos"] == {(2, 3, 3)}
    assert resultado["agua"] == set()
    assert len(resultado["celdas"]) == 1


def test_aplicar_disparo_agua():
    cubo = tablero.crear_cubo(5)
    municion = armamento.municion_inicial()

    resultado = armamento.aplicar_disparo(
        "T", cubo, (2, 3, 3), set(), municion
    )

    assert resultado["agua"] == {(2, 3, 3)}
    assert resultado["impactos"] == set()


def test_no_repetir_disparo():
    cubo = tablero.crear_cubo(5)
    municion = armamento.municion_inicial()

    disparos = {(2, 3, 3)}

    resultado = armamento.aplicar_disparo(
        "T", cubo, (2, 3, 3), {(2, 3, 3)},
        municion, disparos_previos=disparos
    )

    assert resultado["celdas"] == set()


def test_arma_invalida():
    cubo = tablero.crear_cubo(5)

    resultado = armamento.disparar("X", cubo, (2, 2, 2))

    assert resultado == set()
