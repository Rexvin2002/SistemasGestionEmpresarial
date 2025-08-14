#
# Kevin Gómez Valderas 2ºDAM
#
#
# MÉTODOS
#
def longitudes_cadenas(lista_cadenas):

    return [len(cadena) for cadena in lista_cadenas]


#
# USO
#
cadenas = ["Hola", "Python", "Mundo", "Programación"]
longitudes = longitudes_cadenas(cadenas)

print("Lista de cadenas:", cadenas)
print("Longitudes de las cadenas:", longitudes)
