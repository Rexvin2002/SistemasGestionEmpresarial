#
# Kevin Gómez Valderas 2ºDAM
#
#
# MAIN
#
def main():

    while True:

        a, b = map(
            float, input("Introduzca dos números separados por espacio: ").split()
        )

        dividir = lambda a, b: a / b

        try:

            resultado = dividir(a, b)
            print("Resultado de la división:", resultado, "\n")

        except ZeroDivisionError:

            print("Error: No se puede dividir entre cero.")
            print("Prueba otra vez.\n")

        continuar = input("¿Desea continuar? (s/n): ").strip().lower()
        print()

        if continuar != "s":

            print("Gracias por usar el programa. ¡Hasta luego!")
            break


main()
