


# Kevin Gómez 2ºDAM

# 5. Funcion que transforma una cadena en el reverso (“Hola Mundo” a “odnuM aloH”).
# Transforma la cadena en lista, utiliza el reverse y pasa la lista a cadena.

def reverso_cadena(cadena):
    # Convierte la cadena en una lista de caracteres
    lista_caracteres = list(cadena)
    # Invierte la lista usando el método reverse
    lista_caracteres.reverse()
    # Convierte la lista nuevamente en una cadena
    cadena_invertida = ''.join(lista_caracteres)
    return cadena_invertida

# Ejemplo de uso
cadena = "Hola Mundo"
resultado = reverso_cadena(cadena)
print(resultado)  # Salida: "odnuM aloH"
