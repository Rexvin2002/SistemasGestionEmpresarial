


# Kevin Gómez 2ºDAM

"""
8. Escribir un programa que cree un diccionario de traducción español-inglés. Con las
siguientes opciones
1. Añadir palabras al diccionario. El usuario introducirá las palabras en español e inglés
separadas por dos puntos, y cada par `<palabra>:<traducción>` separados por comas. El
programa debe crear un diccionario con las palabras y sus traducciones.
2. Traducir. Se pedirá una frase en español y utilizará el diccionario para traducirla palabra
a palabra. Si una palabra no está en el diccionario debe dejarla sin traducir.
Puede ser útil el método split.
"""

def menu():
    print("\nMenú de Diccionario de Traducción:")
    print("1. Añadir palabras al diccionario")
    print("2. Traducir una frase")
    print("3. Salir")

# Diccionario de traducción
diccionario_traduccion = {}

# Añadir palabras
# Separar cada par de palabras mediante la coma
# Luego divide el par mediante los dos puntos
# Añade el par al diccionario eliminando espacios laterales de la palabra
# En el caso de no añadir el formato correcto salta un error
def añadir_palabras():
    entrada = input("Introduce las palabras en el formato <español>:<inglés> separadas por comas: ")
    pares = entrada.split(",")  
    for par in pares:
        try:
            palabra_es, palabra_en = par.split(":")  
            diccionario_traduccion[palabra_es.strip()] = palabra_en.strip()  
            print(f"'{palabra_es.strip()}' añadido como '{palabra_en.strip()}'.")
        except ValueError:
            print(f"Error al procesar el par '{par}'. Asegúrate de usar el formato <español>:<inglés>.")

# Traducir
# Traduce una frase en español introducida por el usuario
# Se divide la frase en palabras sueltas y se almacenan en una lista
# Se crea una lista para almacenar la traducción
# Si la palabra está en el diccionario, se traduce; si no, se deja tal cual
# Finalmente muestra la frase traducida
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

# Gestión de opciones
# Establece la funcion referente a la opcion elegida
while True:
    menu()
    opcion = input("\nElige una opción: ")
    
    if opcion == '1':
        añadir_palabras()
    elif opcion == '2':
        traducir_frase()
    elif opcion == '3':
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Por favor, elige una opción del menú.")