


# Kevin Gómez 2ºDAM

# 2. Función división controlada, pedimos a y b, y realiza la división, y si da algún error (típico b
# vale 0) la función devuelve 0. (Hacer con un bloque try)

def main():
    while True:
        # Pedir dos números en una sola línea separados por un espacio
        a, b = map(float, input("Introduzca dos números separados por espacio: ").split())

        # Se define una función lambda que divide a entre b
        dividir = lambda a, b: a / b

        try:
            # Llamar a la función lambda y mostrar el resultado
            resultado = dividir(a, b)
            print("Resultado de la división:", resultado, "\n")
        except ZeroDivisionError:
            print("Error: No se puede dividir entre cero.")
            print("Prueba otra vez.\n")

        # Preguntar al usuario si desea continuar o detener el bucle
        continuar = input("¿Desea continuar? (s/n): ").strip().lower()
        print()  # Añadir una línea en blanco para mejorar la legibilidad
        if continuar != 's':
            print("Gracias por usar el programa. ¡Hasta luego!")
            break

main()