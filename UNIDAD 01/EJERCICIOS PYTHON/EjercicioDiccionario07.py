


# Kevin Gómez 2ºDAM

"""
7. Utilizando diccionarios un programa de “gestión de frutería” que muestre las siguientes
opciones de menú hasta que se decida finalizar:
- Añadir un articulo a la frutería. Pedimos nombre y precio por kilo. Se guardan en un
diccionario.
- Mostrar tienda (ver todos los artículos y precios).
- Crear una cesta de la compra. La cesta de la compra es un diccionario. Eliminamos todos
los items de ese diccionario.
- Añadir artículo a la cesta. Preguntamos por fruta y cantidad de kilos. En el diccionario se
guardan el artículo y el total (kilos por precio por kilo).
- Calcular total de la cesta.
"""

def menu():
    # Se muestra el menú de opciones
    print("\nMenú de Frutería:")
    print("1. Añadir artículo a la frutería")
    print("2. Mostrar tienda")
    print("3. Crear una cesta de la compra (vaciar cesta actual)")
    print("4. Añadir artículo a la cesta")
    print("5. Calcular total de la cesta")
    print("6. Salir")

# Diccionario para la tienda (nombre de fruta y precio por kilo)
tienda = {}

# Diccionario para la cesta de la compra (nombre de fruta y precio total)
cesta_compra = {}

# Añade un artículo en la lista tienda preguntando el nombre y el precio por kilo de la fruta
# El nombre de la fruta se resalta poniendolo en mayúsculas mediante .capitalize()
# En caso de que no se introduzca un valor válido para el precio salta un mensaje de error.
def añadir_articulo_tienda():
    nombre = input("Introduce el nombre de la fruta: ").capitalize()
    try:
        precio = float(input(f"Introduce el precio por kilo de {nombre}: "))
        tienda[nombre] = precio
        print(f"{nombre} añadido a la tienda a {precio} €/kilo.")
    except ValueError:
        print("Error: Por favor, introduce un valor válido para el precio.")

# Muestra todos el nombre y el precio por kilo de todos los artículos almacenados 
# en la fruteria es decir, la lista tienda 
# Se emplea un bucle for en el que se extraen los pares clave-valor de la lista tienda mediante .items
# En caso de que esté vacia se muestra un mensaje
def mostrar_tienda():
    if tienda:
        print("\nArtículos disponibles en la tienda:")
        for fruta, precio in tienda.items():
            print(f"{fruta}: {precio} €/kilo")
    else:
        print("La tienda está vacía.")

# Modifica la lista creada anteriormente fuera de la funcion mediante global.
# Vacia la lista para volver a añadir productos en la cesta
def crear_cesta():
    global cesta_compra
    cesta_compra = {}
    print("Cesta de la compra vaciada.")

# Añade un artículo a la cesta
# Comprueba si la tienda está vacia o no, en el caso de que lo esté salta un mensaje de advertencia
# En el caso de que el nombre de la fruta no se encuentre en la tienda salta un mensaje
# A continuación se pregunta la cantidad de kilos que se quieren añadir
# Si la cantidad es 0 salta un mensaje para que introduzca un numero mayor a 0
# Finalmente se calcula el precio final multiplicando los kilos adquiridos por el 
# precio por kilos al que se vende y se almacena en la cesta de la compra
def añadir_articulo_cesta():
    if not tienda:
        print("La tienda está vacía. Añade artículos a la tienda primero.")
        return

    nombre = input("Introduce el nombre de la fruta que quieres añadir a la cesta: ").capitalize()
    
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
        print(f"{kilos} kilos de {nombre} añadidos a la cesta por un total de {precio_total:.2f} €.")
    except ValueError:
        print("Error: Por favor, introduce un valor válido para los kilos.")

# Se calcula el precio total de la cesta
# Comprueba si la cesta está vacia y lanza un mensaje de aviso
# En el caso contrario se calcula el total sumando todos los valores 
# de la lista de la cesta
def calcular_total_cesta():
    if cesta_compra:
        total = sum(cesta_compra.values())
        print(f"\nEl total de la cesta es: {total:.2f} €.")
    else:
        print("La cesta está vacía.")

# Gestión de menú
# Ejecuta una función referida a la opción elegida
# En el caso de que la opcion no sea válida salta un aviso
while True:
    menu()
    opcion = input("\nElige una opción: ")

    if opcion == '1':
        añadir_articulo_tienda()
    elif opcion == '2':
        mostrar_tienda()
    elif opcion == '3':
        crear_cesta()
    elif opcion == '4':
        añadir_articulo_cesta()
    elif opcion == '5':
        calcular_total_cesta()
    elif opcion == '6':
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Por favor, elige una opción del menú.")
