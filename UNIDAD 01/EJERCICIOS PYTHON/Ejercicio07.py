


# Kevin Gómez 2ºDAM

"""
7. La conjetura de Collatz dice que
Sea la siguiente operación, aplicable a cualquier número entero positivo:
• Si el número es par, se divide entre 2.
• Si el número es impar, se multiplica por 3 y se suma 1.
Siempre se va a llegar al número 1
Del 1 al 100 comprueba que se cumple. Guarda en una lista de listas el “recorrido” para cada
número del uno al 100. Muestra que número tiene el “recorrido” más largo. Optimiza el
algoritmo de manera que si durante el cálculo del camino llegas a un paso que está calculado
(por ejemplo, llegas al 24, pero la lista de todos los pasos para el 24 ya la tienes guardada),
no recalcules, sino simplemente añade la lista ya calculada al resultado.
"""

def collatz_sequence(n, memo):
    #Devuelve el recorrido de Collatz para el número n, usando memoización.
    if n in memo:
        return memo[n]
    
    original_n = n
    sequence = [n]
    
    while n != 1:
        if n in memo:
            sequence.extend(memo[n][1:])  # Agregar la parte de la secuencia ya calculada
            break
        
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        
        sequence.append(n)
    
    memo[original_n] = sequence
    return sequence

def main():
    memo = {}
    recorridos = []

    for i in range(1, 101):
        sec = collatz_sequence(i, memo)
        recorridos.append(sec)
    
    # Encontrar el recorrido más largo
    max_length = 0
    number_with_max_length = 0
    
    for seq in recorridos:
        if len(seq) > max_length:
            max_length = len(seq)
            number_with_max_length = seq[0]
    
    print("Número con el recorrido más largo:", number_with_max_length)
    print("Longitud del recorrido:", max_length)

    # Opcional: Mostrar todos los recorridos
    for idx, recorrido in enumerate(recorridos, 1):
        print(f"Recorrido para {idx}: {recorrido} \n")

if __name__ == "__main__":
    main()

"""
Prueba--------------------------------------

def main():
    while True:
        try:
            # Pide al usuario que introduzca un 3número
            num = float(input("Introduzca un número (o 'salir' para terminar): "))

            if num % 2 == 0:
                # Define una función lambda para dividir por 2 y se muestra el resultado
                division = lambda x: x // 2
                print("El resultado es", division(num), "\n")
            else:
                # Define una función lambda para multiplicar por 3 y sumar 1 y muestra el resultado
                multi = lambda x: int(x * 3) + 1
                print("El resultado es", multi(num), "\n")

        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")
main()
"""