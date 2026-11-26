# OPERACIÓN CUBO

## Batalla Naval 3D

Trabajo Práctico Integrador de **Programación 1**.

El proyecto consiste en desarrollar un juego de Batalla Naval en tres dimensiones, utilizando un cubo representado mediante matrices anidadas.

## Integrantes

* Federico Mara
* Abril Uberti
* Mariana Bogarin
* Franco Fernandez
* Tiziano Ginel
* Luciana Olivieri

## Instalación

El proyecto requiere:

* Python 3.10 o superior

Para verificar la versión de Python:

```bash
python --version
```

Para instalar las dependencias (solo hace falta para correr los tests):

```bash
pip install -r requirements.txt
```

## Ejecución

Para ejecutar el programa:

```bash
python main.py
```

Para correr las pruebas unitarias:

```bash
pytest
```

## Cómo jugar

**Menú principal**: elegir con el número de opción (1 a 5): partida
uno contra uno, uno contra la máquina, máquina contra máquina,
continuar una partida guardada, o salir.

Contra la máquina, además se elige su dificultad (fácil: dispara al
azar; difícil: remata con torpedo guiado una nave que ya impactó).

**Ubicación de la flota**: antes de cada partida, cada jugador humano
elige si ubica su flota de forma manual o automática (la máquina
siempre la ubica automática). En modo manual se pide la letra de la
nave (F = Fragata, D = Destructor, S = Submarino, C = Crucero,
P = Portaaviones, E = Estación orbital) y el tramo que ocupa en
formato `z,x,y-z,x,y` (por ejemplo `3,5,4-3,5,5`).

Cada nave tiene su comportamiento propio: el Destructor revela una
celda ocupada del rival al ser impactado, el Submarino es inmune al
barrido láser, el Portaaviones necesita dos impactos por celda, y la
Estación orbital otorga munición extra al hundirse.

**Turno**: en cada turno se elige una de estas opciones:

1. Disparar: se pide el arma (T/R/C/S/L/O/G) y el objetivo `z,x,y`
   (para el láser o el sonar, también el eje).
2. Ver el cubo: muestra una capa (z) del propio tablero.
3. Guardar y salir: guarda la partida con un nombre y vuelve al menú.
4. Ejecutar un recorrido: corre uno de los recorridos del cubo
   (`capas`, `inverso` o `propagacion`) sobre el propio tablero.

**Al terminar la partida** se muestra un resumen (turnos jugados,
disparos/impactos/aguas de cada jugador) y el ranking acumulado de
victorias, y se puede exportar el historial de jugadas a un CSV.

## Estructura del proyecto

El proyecto se encuentra dividido en módulos:

* `tablero.py`: creación y manejo del cubo y operaciones con matrices.
* `flota.py`: naves y ubicación de la flota.
* `radar.py`: búsquedas y recorridos.
* `armamento.py`: armas y disparos.
* `registro.py`: historial y partidas guardadas.
* `partida.py`: funcionamiento de las partidas.
* `main.py`: entrada y salida del programa.

## Estado del proyecto

El proyecto se desarrolla progresivamente de acuerdo con las distintas etapas establecidas para el Trabajo Práctico.
