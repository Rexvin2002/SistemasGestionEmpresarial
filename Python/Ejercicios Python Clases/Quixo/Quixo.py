#
# Kevin Gómez Valderas 2ºDAM
#
import random
import time


#
# MÉTODOS
#
def dibujar_tablero(tablero):

    print("\n    1   2   3   4   5")
    print("  ---------------------")

    for i in range(5):

        print(f"{i+1} | {' | '.join(tablero[i])} |")

        if i < 4:
            print("  ---------------------")


def verificar_ganador(tablero, simbolo):

    return (
        any(all(casilla == simbolo for casilla in fila) for fila in tablero)
        or any(
            all(tablero[fila][col] == simbolo for fila in range(5)) for col in range(5)
        )
        or all(tablero[i][i] == simbolo for i in range(5))
        or all(tablero[i][4 - i] == simbolo for i in range(5))
    )


def obtener_movimiento_ia(opciones):

    print("\nIA pensando", end="")

    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.5)

    print()
    return random.choice(opciones)


def realizar_movimiento(tablero, fila, col, direccion, simbolo):

    if direccion == "arriba":

        for r in range(fila, 0, -1):
            tablero[r][col] = tablero[r - 1][col]

        tablero[0][col] = simbolo

    elif direccion == "abajo":

        for r in range(fila, 4):
            tablero[r][col] = tablero[r + 1][col]

        tablero[4][col] = simbolo

    elif direccion == "izquierda":

        for c in range(col, 0, -1):
            tablero[fila][c] = tablero[fila][c - 1]

        tablero[fila][0] = simbolo

    elif direccion == "derecha":

        for c in range(col, 4):
            tablero[fila][c] = tablero[fila][c + 1]

        tablero[fila][4] = simbolo


def obtener_direcciones_validas(fila, col):

    direcciones = []

    if fila == 0:

        direcciones.append("abajo")

    if fila == 4:

        direcciones.append("arriba")

    if col == 0:

        direcciones.append("derecha")

    if col == 4:

        direcciones.append("izquierda")

    if 0 < fila < 4:

        direcciones.extend(["arriba", "abajo"])

    if 0 < col < 4:

        direcciones.extend(["izquierda", "derecha"])

    return direcciones


def jugar():

    tablero = [[" "] * 5 for _ in range(5)]
    posiciones_validas = [(r, c) for r in [0, 4] for c in range(5)] + [
        (r, c) for r in range(1, 4) for c in [0, 4]
    ]

    print("\n--¡BIENVENIDO A QUIXO!--")

    while True:

        eleccion = input("\nElige tu símbolo (1 para X, 2 para O): ")

        if eleccion in ("1", "2"):

            jugador, ia = ("X", "O") if eleccion == "1" else ("O", "X")
            break

    turno_actual = jugador

    while True:

        dibujar_tablero(tablero)
        print(f"\nTurno de {turno_actual}")

        if turno_actual == ia:

            while True:

                fila, col = random.choice(posiciones_validas)

                if tablero[fila][col] in (" ", ia):
                    break

            print(f"IA elige posición {fila+1},{col+1}")

        else:

            while True:

                try:

                    fila, col = map(
                        int,
                        input(
                            "Ingresa fila y columna (1-5) para elegir (ej. '1 2'): "
                        ).split(),
                    )

                    fila -= 1
                    col -= 1

                    if (fila, col) in posiciones_validas and tablero[fila][col] in (
                        " ",
                        jugador,
                    ):
                        break
                    print("Posición inválida o no es tu símbolo. Intenta nuevamente.")

                except:
                    print("Ingresa dos números entre 1-5 separados por espacio.")

        direcciones = obtener_direcciones_validas(fila, col)

        if turno_actual == ia:

            direccion = obtener_movimiento_ia(direcciones)

        else:

            while True:

                direccion = input(
                    f"Elige dirección ({'/'.join(direcciones)}): "
                ).lower()

                if direccion in direcciones:
                    break

                print("Dirección inválida. Intenta nuevamente.")

        realizar_movimiento(tablero, fila, col, direccion, turno_actual)

        if verificar_ganador(tablero, turno_actual):

            dibujar_tablero(tablero)
            print(f"\n¡El jugador {turno_actual} gana!\n")
            break

        turno_actual = ia if turno_actual == jugador else jugador


#
# MAIN
#
if __name__ == "__main__":
    jugar()
