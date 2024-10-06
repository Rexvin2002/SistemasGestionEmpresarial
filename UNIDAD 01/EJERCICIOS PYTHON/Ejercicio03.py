


# Kevin Gómez 2ºDAM

# 3. Funcion que a partir de una lista de cadenas cree una lista con las longitudes de las cadenas.
# Utiliza List Comprehension.

# Función que utiliza un list comprehension para obtener la longitud de cada cadena en la lista
def longitudes_cadenas(lista_cadenas):
    return [len(cadena) for cadena in lista_cadenas]

# Ejemplo de uso:
cadenas = ["Hola", "Python", "Mundo", "Programación"]
longitudes = longitudes_cadenas(cadenas)
print("Lista de cadenas:", cadenas)
print("Longitudes de las cadenas:", longitudes)
