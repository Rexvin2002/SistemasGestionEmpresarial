#
# Kevin Gómez Valderas 2ºDAM
#
#
# MÉTODOS
#
def menu():

    print("\nMenú de Frutería:")
    print("1. Añadir artículo a la frutería")
    print("2. Mostrar tienda")
    print("3. Crear una cesta de la compra (vaciar cesta actual)")
    print("4. Añadir artículo a la cesta")
    print("5. Calcular total de la cesta")
    print("6. Salir")


tienda = {}
cesta_compra = {}


def añadir_articulo_tienda():

    nombre = input("Introduce el nombre de la fruta: ").capitalize()

    try:

        precio = float(input(f"Introduce el precio por kilo de {nombre}: "))
        tienda[nombre] = precio

        print(f"{nombre} añadido a la tienda a {precio} €/kilo.")

    except ValueError:

        print("Error: Por favor, introduce un valor válido para el precio.")


def mostrar_tienda():

    if tienda:

        print("\nArtículos disponibles en la tienda:")

        for fruta, precio in tienda.items():

            print(f"{fruta}: {precio} €/kilo")

    else:

        print("La tienda está vacía.")


def crear_cesta():

    global cesta_compra
    cesta_compra = {}

    print("Cesta de la compra vaciada.")


def añadir_articulo_cesta():

    if not tienda:

        print("La tienda está vacía. Añade artículos a la tienda primero.")
        return

    nombre = input(
        "Introduce el nombre de la fruta que quieres añadir a la cesta: "
    ).capitalize()

    if nombre not in tienda:

        print(f"{nombre} no está disponible en la tienda.")
        return

    try:

        kilos = float(input(f"¿Cuántos kilos de {nombre} quieres añadir?: "))

        if kilos <= 0:
            print("La cantidad debe ser mayor que 0.")
            return

        precio_total = tienda[nombre] * kilos
        cesta_compra[nombre] = precio_total

        print(
            f"{kilos} kilos de {nombre} añadidos a la cesta por un total de {precio_total:.2f} €."
        )

    except ValueError:

        print("Error: Por favor, introduce un valor válido para los kilos.")


def calcular_total_cesta():
    if cesta_compra:
        total = sum(cesta_compra.values())
        print(f"\nEl total de la cesta es: {total:.2f} €.")
    else:
        print("La cesta está vacía.")


#
# USO
#
while True:

    menu()

    opcion = input("\nElige una opción: ")

    if opcion == "1":

        añadir_articulo_tienda()

    elif opcion == "2":

        mostrar_tienda()

    elif opcion == "3":

        crear_cesta()

    elif opcion == "4":

        añadir_articulo_cesta()

    elif opcion == "5":

        calcular_total_cesta()

    elif opcion == "6":

        print("Saliendo del programa...")
        break

    else:

        print("Opción no válida. Por favor, elige una opción del menú.")
