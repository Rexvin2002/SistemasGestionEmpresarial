


# Kevin Gómez 2ºDAM

# 4. Funcion de binario (pasamos una cadena de texto con 1 y 0, y convertimos la cadena en
# lista) a decimal y de decimal a binario.

# De binario a decimal
# La función convierte una cadena de texto con 1s y 0s en un número decimal mediante la función int() 
# con base 2 para convertir de binario a decimal (Los valores posibles de base son del 2 al 36. 
# El valor por defecto es 10 (decimal).)
def binario_a_decimal(binario):
    try:
        return int(binario, 2)
    except ValueError:
        raise ValueError("La cadena de texto debe contener solo 1s y 0s.")

# Ejemplo de uso
cadena_binaria = "1101"  # 13 en decimal
print(f"El número decimal de {cadena_binaria} es {binario_a_decimal(cadena_binaria)}")


# De decimal a binario
# Convierte un número decimal en una cadena de texto binaria mediante la función bin() y 
# eliminando el prefijo '0b' añadiendo [2:]
def decimal_a_binario(decimal):
    if decimal < 0:
        raise ValueError("El número decimal debe ser no negativo.")
    return bin(decimal)[2:]

# Ejemplo de uso
numero_decimal = 13
print(f"El número binario de {numero_decimal} es {decimal_a_binario(numero_decimal)}")