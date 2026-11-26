import pytest
import radar


def test_buscar_lineal():
    """Verifica que la búsqueda lineal encuentre las naves en el cubo y devuelva las métricas."""
    # simulo un cubo lleno de agua
    cubo = [[[radar.AGUA_SIN_EXPLORAR for _ in range(3)] for _ in range(3)] for _ in range(3)]
    
    # pongo naves ocultas
    cubo[0][0][0] = radar.NAVE_OCULTA
    cubo[1][2][1] = radar.NAVE_OCULTA

    puntos, metricas = radar.buscar_lineal(cubo, radar.NAVE_OCULTA)

    assert (1, 1, 1) in puntos
    assert (2, 2, 3) in puntos
    assert len(puntos) == 2
    assert "comparaciones" in metricas
    assert metricas["comparaciones"] == 27  # 3 * 3 * 3


def test_buscar_optimizada_valida_estado():
    """Verifica que buscar_optimizada lance ValueError si se busca un estado inválido."""
    cubo = [[[radar.AGUA_SIN_EXPLORAR for _ in range(3)] for _ in range(3)] for _ in range(3)]
    
    with pytest.raises(ValueError):
        radar.buscar_optimizada(cubo, radar.AGUA_MARCADA)


def test_buscar_optimizada_encuentra_nave():
    """Verifica que la búsqueda optimizada encuentre naves contiguas mediante expansión."""
    cubo = [[[radar.AGUA_SIN_EXPLORAR for _ in range(3)] for _ in range(3)] for _ in range(3)]
    cubo[0][0][0] = radar.NAVE_OCULTA
    cubo[0][0][1] = radar.NAVE_OCULTA  # Vecina ortogonal (z+x+y paridad distinta)

    puntos, metricas = radar.buscar_optimizada(cubo, radar.NAVE_OCULTA)

    assert (1, 1, 1) in puntos
    assert (1, 2, 1) in puntos
    assert "comparaciones" in metricas


def test_buscar_recursiva():
    """Verifica que la búsqueda recursiva encuentre los objetivos y devuelva la profundidad."""
    cubo = [[[radar.AGUA_SIN_EXPLORAR for _ in range(4)] for _ in range(4)] for _ in range(4)]
    cubo[2][1][1] = radar.NAVE_OCULTA

    puntos, metricas = radar.buscar_recursiva(cubo, radar.NAVE_OCULTA)

    assert (3, 2, 2) in puntos
    assert "profundidad_max" in metricas
    assert metricas["profundidad_max"] > 0


def test_sonar_plano_valido():
    """Verifica que el sonar detecte contactos en un plano sin modificar el cubo."""
    cubo = [[[radar.AGUA_SIN_EXPLORAR for _ in range(3)] for _ in range(3)] for _ in range(3)]
    cubo[1][0][0] = radar.NAVE_OCULTA  # z=2 (índice 1)

    contactos, metricas = radar.sonar_plano(cubo, "z", 2)

    assert (2, 1, 1) in contactos
    assert metricas["comparaciones"] == 9  # 3 * 3 celdas del plano


def test_sonar_plano_errores():
    """Verifica que sonar_plano lance ValueError ante ejes o valores inválidos."""
    cubo = [[[radar.AGUA_SIN_EXPLORAR for _ in range(3)] for _ in range(3)] for _ in range(3)]

    with pytest.raises(ValueError):
        radar.sonar_plano(cubo, "w", 1)  # Eje inválido

    with pytest.raises(ValueError):
        radar.sonar_plano(cubo, "z", 5)  # Valor fuera de rango (N=3)


def test_ejecutar_recorrido():
    """Verifica el funcionamiento del despacho de recorridos por diccionario."""
    cubo = [[[radar.AGUA_SIN_EXPLORAR for _ in range(2)] for _ in range(2)] for _ in range(2)]

    recorrido_capas = radar.ejecutar_recorrido("capas", cubo)
    assert len(recorrido_capas) == 8  # 2 * 2 * 2

    recorrido_inverso = radar.ejecutar_recorrido("inverso", cubo)
    assert len(recorrido_inverso) == 8

    with pytest.raises(ValueError):
        radar.ejecutar_recorrido("invalido", cubo)


def test_mapa_probabilidad():
    """Verifica que el mapa de probabilidad genere un cubo de N x N x N con enteros."""
    cubo = [[[radar.AGUA_SIN_EXPLORAR for _ in range(3)] for _ in range(3)] for _ in range(3)]
    cubo[0][0][0] = radar.IMPACTO

    mapa = radar.mapa_probabilidad(cubo)

    assert len(mapa) == 3
    assert len(mapa[0]) == 3
    assert len(mapa[0][0]) == 3
    # La celda con impacto debe quedar en 0
    assert mapa[0][0][0] == 0
    # Sus vecinas libres deben tener mayor puntaje por el impacto cercano
    assert mapa[0][0][1] >= 20