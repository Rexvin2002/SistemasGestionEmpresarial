


# Kevin Gómez 2ºDAM

#1. Programa que pida un número hasta que el número introducido sea 0 o un número primo. Se
# dará el mensaje “El número 22 no es primo, repite “.

# Método que comprueba si el número indicado es primo o no
def esPrimo(numero):
    # Los números menores o iguales a 1 no son primos
    if numero <= 1:
        return False
    # Comprueba la divisibilidad de 2 hasta la raíz cuadrada del número
    for i in range(2, int(numero**0.5) + 1):
        if numero % i == 0:  # Si es divisible por cualquier número distinto de 1 y de sí mismo
            return False
    return True

# Programa principal el cual muestra un mensaje según si el valor introducido es 0, primo o no.
def main():    
    while True:
        num = int(input("Introduzca un número (0 para salir): "))
        if num == 0:
            print("El programa ha finalizado")
            break
        elif esPrimo(num):
            print(f"El número {num} es primo.")
            break
        else: 
            print(f"El número {num} no es primo, repite.")
main()