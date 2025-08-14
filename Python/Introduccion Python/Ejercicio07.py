#
# Kevin Gómez Valderas 2ºDAM
#
#
# MÉTODOS
#
def collatz_sequence(n, memo):

    if n in memo:

        return memo[n]

    original_n = n
    sequence = [n]

    while n != 1:

        if n in memo:

            sequence.extend(memo[n][1:])
            break

        if n % 2 == 0:

            n = n // 2

        else:

            n = 3 * n + 1

        sequence.append(n)

    memo[original_n] = sequence
    return sequence


#
# MAIN
#
def main():

    memo = {}
    recorridos = []

    for i in range(1, 101):

        sec = collatz_sequence(i, memo)
        recorridos.append(sec)

    max_length = 0
    number_with_max_length = 0

    for seq in recorridos:
        if len(seq) > max_length:
            max_length = len(seq)
            number_with_max_length = seq[0]

    print("Número con el recorrido más largo:", number_with_max_length)
    print("Longitud del recorrido:", max_length)

    for idx, recorrido in enumerate(recorridos, 1):

        print(f"Recorrido para {idx}: {recorrido} \n")


#
# PRUEBA
#
"""
def main():

    while True:

        try:

            num = float(input("Introduzca un número (o 'salir' para terminar): "))

            if num % 2 == 0:

                division = lambda x: x // 2
                print("El resultado es", division(num), "\n")

            else:

                multi = lambda x: int(x * 3) + 1
                print("El resultado es", multi(num), "\n")

        except ValueError:

            print("Entrada no válida. Por favor, ingrese un número.")


main()
"""

#
# USO
#
if __name__ == "__main__":

    main()
