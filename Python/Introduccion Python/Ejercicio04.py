#
# Kevin Gómez Valderas 2ºDAM
#
#
# MÉTODOS
#
def binario_a_decimal(binario):

    try:

        return int(binario, 2)

    except ValueError:

        raise ValueError("La cadena de texto debe contener solo 1s y 0s.")


def decimal_a_binario(decimal):

    if decimal < 0:

        raise ValueError("El número decimal debe ser no negativo.")

    return bin(decimal)[2:]


#
# USO
#
cadena_binaria = "1101"  # 13 en decimal
print(f"El número decimal de {cadena_binaria} es {binario_a_decimal(cadena_binaria)}")

numero_decimal = 13
print(f"El número binario de {numero_decimal} es {decimal_a_binario(numero_decimal)}")
