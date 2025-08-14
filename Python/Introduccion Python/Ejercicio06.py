#
# Kevin Gómez Valderas 2ºDAM
#
#
# MÉTODOS
#
def mayor_en_cada_posicion(lista1, lista2):

    if len(lista1) != len(lista2):

        raise ValueError("Las listas deben tener la misma longitud")

    lista_mayores = list(map(lambda x, y: max(x, y), lista1, lista2))
    return lista_mayores


#
# USO
#
lista1 = [3, 2, 5]
lista2 = [4, 1, 1]
resultado = mayor_en_cada_posicion(lista1, lista2)
print(resultado)
