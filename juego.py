import random
import time
import os

# ============================================================
#                    PIEL DE PINTURA
#              Juego de consola en Python
# ============================================================

# ------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------

ANCHO = 15
ALTO = 10
TIEMPO_PARTIDA = 180       # 3 minutos
COLORES_NECESARIOS = 5
MAX_JUGADORES = 6

# Símbolos del mapa
VACIO = "·"
PARED = "#"
COLOR = "C"
JUGADOR = "J"
CAZADOR = "X"
CAMUFLAJE = "░"

# ------------------------------------------------------------
# UTILIDADES
# ------------------------------------------------------------

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input("\nPresiona ENTER para continuar...")


def titulo():
    print("=" * 60)
    print("                  PIEL DE PINTURA")
    print("=" * 60)


def mensaje(texto):
    print("\n" + texto)
    time.sleep(1)


# ------------------------------------------------------------
# CLASE JUGADOR
# ------------------------------------------------------------

class Jugador:
    def __init__(self, nombre, numero, x, y):
        self.nombre = nombre
        self.numero = numero
        self.x = x
        self.y = y

        self.colores = 0
        self.capturado = False
        self.camuflado = False
        self.pintura = 3
        self.movimientos = 0

    def simbolo(self):
        if self.capturado:
            return "X"

        if self.camuflado:
            return CAMUFLAJE

        return str(self.numero)

    def mover(self, dx, dy, mapa):
        nuevo_x = self.x + dx
        nuevo_y = self.y + dy

        if 0 <= nuevo_x < ANCHO and 0 <= nuevo_y < ALTO:
            if mapa[nuevo_y][nuevo_x] != PARED:
                self.x = nuevo_x
                self.y = nuevo_y
                self.movimientos += 1
                return True

        return False


# ------------------------------------------------------------
# CLASE CAZADOR
# ------------------------------------------------------------

class Cazador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.capturas = 0

    def mover(self, jugadores, mapa):
        objetivos = [
            jugador for jugador in jugadores
            if not jugador.capturado
        ]

        if not objetivos:
            return

        # Buscar al jugador más cercano
        objetivo = min(
            objetivos,
            key=lambda j: abs(self.x - j.x) + abs(self.y - j.y)
        )

        dx = 0
        dy = 0

        if objetivo.x > self.x:
            dx = 1
        elif objetivo.x < self.x:
            dx = -1

        if objetivo.y > self.y:
            dy = 1
        elif objetivo.y < self.y:
            dy = -1

        # Algunas veces el cazador se mueve aleatoriamente
        if random.random() < 0.25:
            movimientos = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1)
            ]

            dx, dy = random.choice(movimientos)

        nuevo_x = self.x + dx
        nuevo_y = self.y + dy

        if (
            0 <= nuevo_x < ANCHO
            and 0 <= nuevo_y < ALTO
            and mapa[nuevo_y][nuevo_x] != PARED
        ):
            self.x = nuevo_x
            self.y = nuevo_y

    def capturar(self, jugadores):
        for jugador in jugadores:

            if jugador.capturado:
                continue

            distancia = abs(self.x - jugador.x) + abs(self.y - jugador.y)

            if distancia <= 1:

                # El camuflaje puede evitar una captura
                if jugador.camuflado:
                    if random.random() < 0.70:
                        jugador.camuflado = False
                        print(
                            f"\n🫥 {jugador.nombre} escapó gracias "
                            "al camuflaje."
                        )
                        continue

                jugador.capturado = True
                self.capturas += 1

                print(
                    f"\n💥 ¡{jugador.nombre} fue capturado "
                    "por el Cazador de Tinta!"
                )


# ------------------------------------------------------------
# CREAR MAPA
# ------------------------------------------------------------

def crear_mapa():
    mapa = []

    for y in range(ALTO):
        fila = []

        for x in range(ANCHO):

            # Bordes
            if x == 0 or y == 0 or x == ANCHO - 1 or y == ALTO - 1:
                fila.append(PARED)

            # Algunas paredes internas
            elif (
                (x == 4 and y in range(2, 7))
                or (x == 9 and y in range(4, 9))
                or (y == 5 and x in range(6, 11))
            ):
                fila.append(PARED)

            else:
                fila.append(VACIO)

        mapa.append(fila)

    return mapa


# ------------------------------------------------------------
# COLOCAR COLORES
# ------------------------------------------------------------

def colocar_colores(mapa, cantidad):
    colores = []

    while len(colores) < cantidad:

        x = random.randint(1, ANCHO - 2)
        y = random.randint(1, ALTO - 2)

        if mapa[y][x] == VACIO:
            mapa[y][x] = COLOR
            colores.append((x, y))

    return colores


# ------------------------------------------------------------
# POSICIONES
# ------------------------------------------------------------

def posicion_libre(mapa, ocupadas):

    while True:
        x = random.randint(1, ANCHO - 2)
        y = random.randint(1, ALTO - 2)

        if mapa[y][x] == VACIO and (x, y) not in ocupadas:
            return x, y


# ------------------------------------------------------------
# MOSTRAR MAPA
# ------------------------------------------------------------

def mostrar_mapa(mapa, jugadores, cazador):

    copia = [fila[:] for fila in mapa]

    # Jugadores
    for jugador in jugadores:

        if not jugador.capturado:
            copia[jugador.y][jugador.x] = jugador.simbolo()

    # Cazador
    copia[cazador.y][cazador.x] = CAZADOR

    print("\n" + "   " + "".join(str(i % 10) for i in range(ANCHO)))

    for y, fila in enumerate(copia):
        print(f"{y:2} " + "".join(fila))

    print()
    print("Leyenda:")
    print("  # = Obstáculo")
    print("  C = Color")
    print("  X = Cazador")
    print("  1-6 = Jugadores")
    print("  ░ = Jugador camuflado")


# ------------------------------------------------------------
# INFORMACIÓN
# ------------------------------------------------------------

def mostrar_estado(jugadores, cazador, tiempo_restante):

    print("\n" + "-" * 60)
    print(f"⏱️ Tiempo restante: {tiempo_restante} segundos")
    print(f"🎯 Capturas del cazador: {cazador.capturas}")
    print("-" * 60)

    for jugador in jugadores:

        estado = "CAPTURADO" if jugador.capturado else "ACTIVO"

        print(
            f"{jugador.numero}. {jugador.nombre} | "
            f"Colores: {jugador.colores}/{COLORES_NECESARIOS} | "
            f"Pintura: {jugador.pintura} | "
            f"Estado: {estado}"
        )

    print("-" * 60)


# ------------------------------------------------------------
# EXPLORAR
# ------------------------------------------------------------

def explorar(jugador, mapa):

    print("\n🔎 Explorando los alrededores...")

    encontrados = []

    for dy in range(-1, 2):
        for dx in range(-1, 2):

            x = jugador.x + dx
            y = jugador.y + dy

            if (
                0 <= x < ANCHO
                and 0 <= y < ALTO
                and mapa[y][x] == COLOR
            ):
                encontrados.append((x, y))

    if encontrados:
        print("🎨 ¡Hay un color cerca!")
    else:
        print("No encontraste colores cercanos.")

    pausa()


# ------------------------------------------------------------
# RECOGER COLOR
# ------------------------------------------------------------

def recoger_color(jugador, mapa):

    if mapa[jugador.y][jugador.x] == COLOR:

        mapa[jugador.y][jugador.x] = VACIO
        jugador.colores += 1

        print("\n🎨 ¡Has recuperado un color!")

        if jugador.colores >= COLORES_NECESARIOS:
            print(
                f"\n🏆 ¡{jugador.nombre} consiguió todos "
                "los colores!"
            )

        pausa()

    else:
        print("\nAquí no hay ningún color.")
        pausa()


# ------------------------------------------------------------
# CAMUFLAJE
# ------------------------------------------------------------

def activar_camuflaje(jugador):

    if jugador.camuflado:
        print("\nYa estás camuflado.")
        pausa()
        return

    jugador.camuflado = True

    print(
        "\n🫥 Te has camuflado con el entorno."
        "\nEl cazador tendrá más dificultad para capturarte."
    )

    pausa()


# ------------------------------------------------------------
# DISPARAR PINTURA
# ------------------------------------------------------------

def disparar(jugador, cazador):

    if jugador.pintura <= 0:
        print("\n🔫 No tienes pintura.")
        pausa()
        return

    distancia = (
        abs(jugador.x - cazador.x)
        + abs(jugador.y - cazador.y)
    )

    jugador.pintura -= 1

    if distancia <= 3:

        print(
            "\n🎨 ¡DISPARO DE PINTURA!"
            "\nHas alcanzado al Cazador de Tinta."
        )

        # Alejar al cazador
        dx = cazador.x - jugador.x
        dy = cazador.y - jugador.y

        if dx != 0:
            cazador.x += 1 if dx > 0 else -1

        if dy != 0:
            cazador.y += 1 if dy > 0 else -1

    else:
        print("\n💨 La pintura no alcanzó al cazador.")

    pausa()


# ------------------------------------------------------------
# REINICIAR CAMUFLAJE
# ------------------------------------------------------------

def actualizar_camuflaje(jugadores):

    for jugador in jugadores:

        if jugador.camuflado:

            # El camuflaje tiene una posibilidad de desaparecer
            if random.random() < 0.20:
                jugador.camuflado = False


# ------------------------------------------------------------
# COMPROBAR VICTORIA
# ------------------------------------------------------------

def comprobar_victoria(jugadores):

    # Victoria si todos los colores fueron recuperados
    activos = [
        jugador for jugador in jugadores
        if not jugador.capturado
    ]

    if not activos:
        return "CAZADOR"

    if all(
        jugador.colores >= COLORES_NECESARIOS
        for jugador in activos
    ):
        return "JUGADORES"

    return None


# ------------------------------------------------------------
# TURNO DEL JUGADOR
# ------------------------------------------------------------

def turno_jugador(jugador, mapa, cazador):

    if jugador.capturado:
        return

    while True:

        limpiar()

        print("=" * 60)
        print(f"             TURNO DE {jugador.nombre}")
        print("=" * 60)

        print(
            f"\n🎨 Colores: "
            f"{jugador.colores}/{COLORES_NECESARIOS}"
        )

        print(f"🔫 Pintura disponible: {jugador.pintura}")

        if jugador.camuflado:
            print("🫥 Estado: CAMUFLADO")

        print("\n¿Qué deseas hacer?")

        print("1. Moverse")
        print("2. Recoger color")
        print("3. Camuflarse")
        print("4. Disparar pintura")
        print("5. Explorar")
        print("6. Pasar turno")

        opcion = input("\n> ")

        # ----------------------------------------------------
        # MOVER
        # ----------------------------------------------------

        if opcion == "1":

            print("\nMovimiento:")
            print("W = Arriba")
            print("S = Abajo")
            print("A = Izquierda")
            print("D = Derecha")

            movimiento = input("> ").lower()

            movimientos = {
                "w": (0, -1),
                "s": (0, 1),
                "a": (-1, 0),
                "d": (1, 0)
            }

            if movimiento in movimientos:

                dx, dy = movimientos[movimiento]

                if jugador.mover(dx, dy, mapa):
                    print("\n🏃 Te has movido.")
                else:
                    print("\n🚧 No puedes atravesar ese lugar.")

                pausa()
                break

            else:
                print("\nMovimiento inválido.")
                pausa()

        # ----------------------------------------------------
        # COLOR
        # ----------------------------------------------------

        elif opcion == "2":
            recoger_color(jugador, mapa)
            break

        # ----------------------------------------------------
        # CAMUFLAJE
        # ----------------------------------------------------

        elif opcion == "3":
            activar_camuflaje(jugador)
            break

        # ----------------------------------------------------
        # DISPARAR
        # ----------------------------------------------------

        elif opcion == "4":
            disparar(jugador, cazador)
            break

        # ----------------------------------------------------
        # EXPLORAR
        # ----------------------------------------------------

        elif opcion == "5":
            explorar(jugador, mapa)
            break

        # ----------------------------------------------------
        # PASAR
        # ----------------------------------------------------

        elif opcion == "6":
            print("\nHas pasado el turno.")
            pausa()
            break

        else:
            print("\nOpción inválida.")
            pausa()


# ------------------------------------------------------------
# INTRODUCCIÓN
# ------------------------------------------------------------

def introduccion():

    limpiar()

    print("""
==============================================================
                     PIEL DE PINTURA
==============================================================

Eres un jugador dentro de un mundo lleno de colores.

Tu misión es recuperar los colores perdidos mientras
trabajas con los demás jugadores para sobrevivir.

Pero hay un problema...

Un jugador será elegido como:

                    CAZADOR DE TINTA

El Cazador deberá encontrar y capturar a los jugadores
antes de que consigan recuperar todos los colores.

Utiliza:

    🎨 Los colores
    🫥 El camuflaje
    🔫 Las pistolas de pintura
    🗺️ El mapa
    🧠 La estrategia

¡Buena suerte!
""")

    pausa()


# ------------------------------------------------------------
# CONFIGURAR JUGADORES
# ------------------------------------------------------------

def configurar_jugadores():

    limpiar()

    titulo()

    print("\nCONFIGURACIÓN DE JUGADORES")
    print("Puedes jugar con 2 a 6 jugadores.")

    while True:

        try:
            cantidad = int(
                input("\nCantidad de jugadores: ")
            )

            if 2 <= cantidad <= MAX_JUGADORES:
                break

            print("Debes introducir entre 2 y 6.")

        except ValueError:
            print("Introduce un número válido.")

    jugadores = []

    for i in range(cantidad):

        while True:

            nombre = input(
                f"Nombre del jugador {i + 1}: "
            ).strip()

            if nombre:
                break

            print("El nombre no puede estar vacío.")

        jugadores.append(nombre)

    return jugadores


# ------------------------------------------------------------
# CREAR PARTIDA
# ------------------------------------------------------------

def crear_partida(nombres):

    mapa = crear_mapa()

    posiciones = []

    jugadores = []

    for i, nombre in enumerate(nombres):

        x, y = posicion_libre(mapa, posiciones)

        posiciones.append((x, y))

        jugadores.append(
            Jugador(
                nombre,
                i + 1,
                x,
                y
            )
        )

    # Colocar colores
    colocar_colores(
        mapa,
        len(nombres) * 2
    )

    # Colocar cazador
    x, y = posicion_libre(mapa, posiciones)

    cazador = Cazador(x, y)

    return mapa, jugadores, cazador


# ------------------------------------------------------------
# SELECCIONAR CAZADOR
# ------------------------------------------------------------

def seleccionar_cazador(jugadores):

    # Elegimos un jugador aleatoriamente
    elegido = random.choice(jugadores)

    print(
        f"\n🎯 El Cazador de Tinta será: "
        f"{elegido.nombre}"
    )

    pausa()

    return elegido


# ------------------------------------------------------------
# JUEGO
# ------------------------------------------------------------

def jugar_partida(nombres):

    mapa, jugadores, cazador = crear_partida(nombres)

    # El jugador elegido para ser cazador
    elegido = seleccionar_cazador(jugadores)

    # Convertimos al jugador elegido en un jugador normal
    # y creamos un cazador controlado por computadora.
    jugadores_activos = [
        jugador
        for jugador in jugadores
        if jugador != elegido
    ]

    # Si hay pocos jugadores, todavía quedan jugadores
    if len(jugadores_activos) == 0:
        return "CAZADOR"

    # El cazador comienza cerca de una zona aleatoria
    x, y = posicion_libre(
        mapa,
        [(j.x, j.y) for j in jugadores]
    )

    cazador.x = x
    cazador.y = y

    tiempo_inicio = time.time()

    turno = 0

    while True:

        # ----------------------------------------------------
        # TIEMPO
        # ----------------------------------------------------

        transcurrido = int(time.time() - tiempo_inicio)

        tiempo_restante = max(
            0,
            TIEMPO_PARTIDA - transcurrido
        )

        # ----------------------------------------------------
        # COMPROBAR TIEMPO
        # ----------------------------------------------------

        if tiempo_restante <= 0:

            limpiar()

            print("""
==============================================================
                         ¡TIEMPO!
==============================================================
""")

            print(
                "⏱️ Se acabó el tiempo."
            )

            pausa()

            return "CAZADOR"

        # ----------------------------------------------------
        # MOSTRAR MAPA
        # ----------------------------------------------------

        limpiar()

        titulo()

        mostrar_mapa(
            mapa,
            jugadores_activos,
            cazador
        )

        mostrar_estado(
            jugadores_activos,
            cazador,
            tiempo_restante
        )

        # ----------------------------------------------------
        # COMPROBAR VICTORIA
        # ----------------------------------------------------

        resultado = comprobar_victoria(
            jugadores_activos
        )

        if resultado:
            return resultado

        # ----------------------------------------------------
        # TURNOS DE JUGADORES
        # ----------------------------------------------------

        for jugador in jugadores_activos:

            if jugador.capturado:
                continue

            # Actualizar tiempo
            transcurrido = int(
                time.time() - tiempo_inicio
            )

            tiempo_restante = max(
                0,
                TIEMPO_PARTIDA - transcurrido
            )

            if tiempo_restante <= 0:
                return "CAZADOR"

            turno_jugador(
                jugador,
                mapa,
                cazador
            )

            # Si el jugador llegó al cazador
            cazador.capturar(jugadores_activos)

            resultado = comprobar_victoria(
                jugadores_activos
            )

            if resultado:
                return resultado

        # ----------------------------------------------------
        # TURNO DEL CAZADOR
        # ----------------------------------------------------

        limpiar()

        print("=" * 60)
        print("                 TURNO DEL CAZADOR")
        print("=" * 60)

        print("\n👹 El Cazador de Tinta está buscando...")

        cazador.mover(
            jugadores_activos,
            mapa
        )

        cazador.capturar(
            jugadores_activos
        )

        actualizar_camuflaje(
            jugadores_activos
        )

        pausa()

        # ----------------------------------------------------
        # COMPROBAR DERROTA
        # ----------------------------------------------------

        resultado = comprobar_victoria(
            jugadores_activos
        )

        if resultado:
            return resultado

        turno += 1


# ------------------------------------------------------------
# RESULTADOS
# ------------------------------------------------------------

def mostrar_resultado(resultado):

    limpiar()

    print("=" * 60)

    if resultado == "JUGADORES":

        print("""
                    🎉 ¡VICTORIA! 🎉

             LOS JUGADORES GANARON

      Se recuperaron todos los colores
      antes de que el tiempo terminara.
""")

    else:

        print("""
                    💥 ¡DERROTA! 💥

             EL CAZADOR DE TINTA GANÓ

      Los jugadores fueron capturados
      o se acabó el tiempo.
""")

    print("=" * 60)

    pausa()


# ------------------------------------------------------------
# REGLAS
# ------------------------------------------------------------

def mostrar_reglas():

    limpiar()

    print("""
==============================================================
                         REGLAS
==============================================================

🎨 OBJETIVO DE LOS JUGADORES
--------------------------------------------------------------
Los jugadores deben encontrar y recuperar los colores
dispersos por el mapa.

Para ganar deben conseguir todos los colores antes
de que sean capturados o termine el tiempo.


👹 CAZADOR DE TINTA
--------------------------------------------------------------
El Cazador intenta localizar y capturar a los jugadores.

Cuando está junto a un jugador puede capturarlo.

El Cazador es controlado automáticamente.


🫥 CAMUFLAJE
--------------------------------------------------------------
Un jugador puede utilizar el camuflaje.

El camuflaje aumenta las posibilidades de escapar
cuando el Cazador intenta capturarlo.


🔫 PISTOLA DE PINTURA
--------------------------------------------------------------
Cada jugador empieza con 3 cargas de pintura.

La pintura puede utilizarse para alejar al Cazador.


🗺️ MAPA
--------------------------------------------------------------
# = Obstáculo
C = Color
X = Cazador
1-6 = Jugadores
░ = Jugador camuflado


⌨️ MOVIMIENTO
--------------------------------------------------------------
W = Arriba
S = Abajo
A = Izquierda
D = Derecha


🏆 VICTORIA
--------------------------------------------------------------
Los jugadores ganan si consiguen todos los colores.

El Cazador gana si todos los jugadores son capturados
o si el tiempo termina.


==============================================================
""")

    pausa()


# ------------------------------------------------------------
# ACERCA DEL JUEGO
# ------------------------------------------------------------

def acerca():

    limpiar()

    print("""
==============================================================
                      PIEL DE PINTURA
==============================================================

Juego multijugador de camuflaje desarrollado para consola.

Inspirado en el diagrama de flujo proporcionado.

Características:

    🎨 Sistema de colores
    🗺️ Mapa
    👥 Jugadores
    👹 Cazador de Tinta
    🫥 Camuflaje
    🔫 Pistolas de pintura
    ⏱️ Tiempo límite
    🏆 Sistema de victoria
    🔄 Repetición de partidas

Versión: 1.0
Lenguaje: Python

==============================================================
""")

    pausa()


# ------------------------------------------------------------
# MENÚ PRINCIPAL
# ------------------------------------------------------------

def menu():

    while True:

        limpiar()

        print("""
==============================================================
                  🎨 PIEL DE PINTURA 🎨
==============================================================

                    1. NUEVA PARTIDA
                    2. REGLAS
                    3. ACERCA DEL JUEGO
                    4. SALIR

==============================================================
""")

        opcion = input("Selecciona una opción: ")

        # ----------------------------------------------------
        # NUEVA PARTIDA
        # ----------------------------------------------------

        if opcion == "1":

            nombres = configurar_jugadores()

            introduccion()

            while True:

                resultado = jugar_partida(
                    nombres
                )

                mostrar_resultado(
                    resultado
                )

                print("""
¿Qué deseas hacer?

1. Jugar otra partida
2. Volver al menú
3. Salir
""")

                opcion_final = input("> ")

                if opcion_final == "1":
                    continue

                elif opcion_final == "2":
                    break

                elif opcion_final == "3":
                    print("\n¡Gracias por jugar Piel de Pintura!")
                    return

                else:
                    print("Opción inválida.")
                    pausa()

        # ----------------------------------------------------
        # REGLAS
        # ----------------------------------------------------

        elif opcion == "2":
            mostrar_reglas()

        # ----------------------------------------------------
        # ACERCA
        # ----------------------------------------------------

        elif opcion == "3":
            acerca()

        # ----------------------------------------------------
        # SALIR
        # ----------------------------------------------------

        elif opcion == "4":

            limpiar()

            print("""
==============================================================
              ¡GRACIAS POR JUGAR!
==============================================================

                    PIEL DE PINTURA

==============================================================
""")

            break

        else:

            print("\nOpción inválida.")
            pausa()


# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------

if __name__ == "__main__":

    try:
        menu()

    except KeyboardInterrupt:

        limpiar()

        print("""
==============================================================
             Juego terminado por el usuario.
==============================================================
""")
