#
# Kevin Gómez Valderas 2ºDAM
#
#
# MÉTODOS
#
def esPrimo(numero):

    if numero <= 1:

        return False

    for i in range(2, int(numero**0.5) + 1):

        if numero % i == 0:
            return False

    return True


#
# MAIN
#
def main():

    while True:

        num = int(input("Introduzca un número (0 para salir): "))

        if num == 0:

            print("El programa ha finalizado")
            break

        elif esPrimo(num):

            print(f"El número {num} es primo.")
            break

        else:

            print(f"El número {num} no es primo, repite.")


main()
