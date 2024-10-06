


# 2. Función división controlada, pedimos a y b, y realiza la división, y si da algún error (típico b
# vale 0) la función devuelve 0. (Hace10 5r con un bloque try)

diccionario = {}

def añadirPalabra:
    entrada = input("Introduce las palabras en el formato <español>:<inglés> separadas por comas: ")
    pares = entrada.split(",")  # Separar cada par de palabras
def traducir:
    

def main():
    while True:
        opcion = input("Escoja una opción:")
        print("1. Añadir palabras al diccionario")
        print("2. Traducir")
        print("3. Salir")
        
        if opcion == 1:
            añadirPalabra()
        elif opcion == 2:
            traducir()
        elif opcion == 3:
            break
        else:
            print("Introduzca una de las opciones disponibles")
    
main()
