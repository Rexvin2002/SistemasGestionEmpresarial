


# Kevin Gómez 2ºDAM

# 6. Genera una funcion que recibe 2 listas. Si son de longitud diferente generamos un error y si
# son de la misma longitud, utilizando map y funcion lambda, generamos una nueva lista con
# el mayor de las dos listas en cada posición (ej: para las listas [3,2,5] y [4,1,1] devuelve
# [4,2,5].

def mayor_en_cada_posicion(lista1, lista2):
    # Verificamos si las listas tienen la misma longitud
    if len(lista1) != len(lista2):
        raise ValueError("Las listas deben tener la misma longitud")
    
    # Utilizamos map y lambda para obtener el mayor en cada posición
    lista_mayores = list(map(lambda x, y: max(x, y), lista1, lista2))
    
    return lista_mayores

# Ejemplo de uso
lista1 = [3, 2, 5]
lista2 = [4, 1, 1]
resultado = mayor_en_cada_posicion(lista1, lista2)
print(resultado)  # Salida: [4, 2, 5]