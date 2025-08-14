#
# Kevin Gómez Valderas 2ºDAM
#
#
# MÉTODOS
#
def reverso_cadena(cadena):

    lista_caracteres = list(cadena)
    lista_caracteres.reverse()
    cadena_invertida = "".join(lista_caracteres)

    return cadena_invertida


#
# USO
#
cadena = "Hola Mundo"
resultado = reverso_cadena(cadena)
print(resultado)  # Salida: "odnuM aloH"
