import armamento
import tablero
import flota
import partida


def _estado_vacio(n=8):
    """Arma un estado 1v1 minimo, sin pasar por los input() de partida.py."""
    cubo_1 = tablero.crear_cubo(n)
    cubo_2 = tablero.crear_cubo(n)
    flota_1 = flota.ubicacion_automatica(cubo_1, flota.CATALOGO_NAVES, semilla=1)
    flota_2 = flota.ubicacion_automatica(cubo_2, flota.CATALOGO_NAVES, semilla=2)

    return {
        "n_max": n,
        "turno_actual": 1,
        "modo": "1v1",
        "jugadores": {
            1: {
                "nombre": "Jugador 1", "cubo": cubo_1, "flota": flota_1,
                "municion": armamento.municion_inicial(), "disparos": set()
            },
            2: {
                "nombre": "Jugador 2", "cubo": cubo_2, "flota": flota_2,
                "municion": armamento.municion_inicial(), "disparos": set()
            }
        },
        "historial": [],
        "ganador": None
    }


def test_hay_ganador_nadie_al_empezar():
    estado = _estado_vacio()
    assert partida.hay_ganador(estado) is None


def test_hay_ganador_cuando_se_hunde_toda_la_flota_rival():
    estado = _estado_vacio()

    for nave in estado["jugadores"][2]["flota"]:
        nave["impactos"] = set(nave["celdas"])
        nave["hundida"] = True

    assert partida.hay_ganador(estado) == "Jugador 1"


def test_es_turno_maquina():
    estado = _estado_vacio()
    estado["modo"] = "vs_maquina"

    estado["turno_actual"] = 1
    assert partida.es_turno_maquina(estado) is False

    estado["turno_actual"] = 2
    assert partida.es_turno_maquina(estado) is True

    estado["modo"] = "maquina_vs_maquina"
    estado["turno_actual"] = 1
    assert partida.es_turno_maquina(estado) is True


def test_ejecutar_turno_impacto_directo():
    estado = _estado_vacio()
    nave = estado["jugadores"][2]["flota"][0]
    celda = sorted(nave["celdas"])[0]

    estado = partida.ejecutar_turno(estado, {"arma": "T", "objetivo": celda})

    assert celda in estado["jugadores"][1]["disparos"]
    assert celda in nave["impactos"]
    assert estado["turno_actual"] == 2
    assert estado["historial"][-1]["resultado"] == "impacto"


def test_ejecutar_turno_no_deja_repetir_disparo():
    estado = _estado_vacio()
    objetivo = (1, 1, 1)

    estado = partida.ejecutar_turno(estado, {"arma": "T", "objetivo": objetivo})
    turno_despues_del_primero = estado["turno_actual"]

    # vuelve a ser el turno de quien disparo primero
    estado["turno_actual"] = 1
    disparos_antes = set(estado["jugadores"][1]["disparos"])

    estado = partida.ejecutar_turno(estado, {"arma": "T", "objetivo": objetivo})

    assert estado["jugadores"][1]["disparos"] == disparos_antes
    assert estado["turno_actual"] == 1  # no avanzo, el disparo se rechazo


def test_ejecutar_turno_submarino_inmune_al_laser():
    estado = _estado_vacio()
    submarino = next(n for n in estado["jugadores"][2]["flota"] if n["letra"] == "S")
    celda = sorted(submarino["celdas"])[0]

    estado = partida.ejecutar_turno(
        estado, {"arma": "L", "objetivo": celda, "eje": "x"}
    )

    assert submarino["impactos"] == set()


def test_portaaviones_necesita_dos_impactos_por_celda():
    estado = _estado_vacio()
    portaaviones = next(n for n in estado["jugadores"][2]["flota"] if n["letra"] == "P")
    celda = sorted(portaaviones["celdas"])[0]

    estado["turno_actual"] = 1
    estado = partida.ejecutar_turno(estado, {"arma": "T", "objetivo": celda})

    assert celda in portaaviones["impactos_parciales"]
    assert celda not in portaaviones["impactos"]

    estado["turno_actual"] = 1
    estado = partida.ejecutar_turno(estado, {"arma": "T", "objetivo": celda})

    assert celda in portaaviones["impactos"]
    assert celda not in portaaviones["impactos_parciales"]


def test_portaaviones_tercer_disparo_a_celda_confirmada_se_rechaza():
    estado = _estado_vacio()
    portaaviones = next(n for n in estado["jugadores"][2]["flota"] if n["letra"] == "P")
    celda = sorted(portaaviones["celdas"])[0]

    for _ in range(2):
        estado["turno_actual"] = 1
        estado = partida.ejecutar_turno(estado, {"arma": "T", "objetivo": celda})

    disparos_antes = set(estado["jugadores"][1]["disparos"])
    estado["turno_actual"] = 1
    estado = partida.ejecutar_turno(estado, {"arma": "T", "objetivo": celda})

    assert estado["jugadores"][1]["disparos"] == disparos_antes


def test_portaaviones_se_hunde_tras_doble_impacto_en_todas_sus_celdas():
    estado = _estado_vacio()
    portaaviones = next(n for n in estado["jugadores"][2]["flota"] if n["letra"] == "P")

    for celda in sorted(portaaviones["celdas"]):
        for _ in range(2):
            estado["turno_actual"] = 1
            estado = partida.ejecutar_turno(estado, {"arma": "T", "objetivo": celda})

    assert portaaviones["hundida"] is True
    assert portaaviones["impactos"] == portaaviones["celdas"]


def test_estado_para_guardar_y_cargar_es_equivalente():
    estado = _estado_vacio()
    estado["turno_actual"] = 2
    estado["jugadores"][1]["disparos"].add((1, 1, 1))

    # dejo un impacto parcial de portaaviones a medio resolver
    portaaviones = next(n for n in estado["jugadores"][2]["flota"] if n["letra"] == "P")
    celda_parcial = sorted(portaaviones["celdas"])[0]
    estado["turno_actual"] = 1
    estado = partida.ejecutar_turno(estado, {"arma": "T", "objetivo": celda_parcial})

    guardado = partida._estado_para_guardar(estado)
    recuperado = partida._estado_desde_guardado(guardado)

    assert recuperado["n_max"] == estado["n_max"]
    assert recuperado["turno_actual"] == estado["turno_actual"]
    assert recuperado["jugadores"][1]["disparos"] == estado["jugadores"][1]["disparos"]

    for original, vuelta in zip(
        estado["jugadores"][2]["flota"], recuperado["jugadores"][2]["flota"]
    ):
        assert original["letra"] == vuelta["letra"]
        assert original["celdas"] == vuelta["celdas"]
        assert original["impactos_parciales"] == vuelta["impactos_parciales"]


def test_crear_jugador_automatico_no_pide_nada():
    jugador = partida._crear_jugador(8, "Máquina", automatico=True)

    assert jugador["nombre"] == "Máquina"
    assert len(jugador["flota"]) == sum(
        datos["cantidad"] for datos in flota.CATALOGO_NAVES.values()
    )
    assert jugador["disparos"] == set()


def test_turno_maquina_dificil_remata_nave_impactada():
    estado = _estado_vacio()
    estado["modo"] = "vs_maquina"
    estado["dificultad"] = "dificil"
    estado["turno_actual"] = 2

    nave = estado["jugadores"][1]["flota"][0]
    celda = sorted(nave["celdas"])[0]
    nave["impactos"].add(celda)

    estado = partida.turno_maquina(estado)

    assert celda in nave["impactos"]
    assert len(nave["impactos"]) >= 1
