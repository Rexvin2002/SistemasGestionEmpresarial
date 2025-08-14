#
# Kevin Gómez Valderas 2ºDAM
#
#
# MÉTODOS
#
def menu():

    print("\nMenú de Diccionario de Traducción:")
    print("1. Añadir palabras al diccionario")
    print("2. Traducir una frase")
    print("3. Salir")


diccionario_traduccion = {}


def añadir_palabras():

    entrada = input(
        "Introduce las palabras en el formato <español>:<inglés> separadas por comas: "
    )
    pares = entrada.split(",")

    for par in pares:

        try:

            palabra_es, palabra_en = par.split(":")
            diccionario_traduccion[palabra_es.strip()] = palabra_en.strip()

            print(f"'{palabra_es.strip()}' añadido como '{palabra_en.strip()}'.")

        except ValueError:

            print(
                f"Error al procesar el par '{par}'. Asegúrate de usar el formato <español>:<inglés>."
            )


def traducir_frase():

    frase = input("Introduce una frase en español: ")
    palabras = frase.split()
    traduccion = []

    for palabra in palabras:

        if palabra in diccionario_traduccion:

            traduccion.append(diccionario_traduccion[palabra])

        else:

            traduccion.append(palabra)

    print("Frase traducida:", " ".join(traduccion))


#
# USO
#
while True:

    menu()
    opcion = input("\nElige una opción: ")

    if opcion == "1":

        añadir_palabras()

    elif opcion == "2":

        traducir_frase()

    elif opcion == "3":

        print("Saliendo del programa...")
        break

    else:

        print("Opción no válida. Por favor, elige una opción del menú.")
