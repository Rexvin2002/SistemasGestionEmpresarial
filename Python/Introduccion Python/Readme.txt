# Ejercicios Python

## Autor: Kevin Gómez Valderas  
## Curso: 2º DAM  

---

## Descripción  
Este repositorio contiene una colección de ejercicios en Python que abordan estructuras de control, listas, diccionarios y funciones. Cada ejercicio está diseñado para practicar diferentes conceptos de programación en Python, siguiendo las mejores prácticas de estilo de codificación.

---

## Ejercicios  

### 1. Números Primos  
**Método:** `esPrimo(numero)`  
**Descripción:**  
- Solicita al usuario un número hasta que se ingrese 0 o un número primo.  
- Muestra mensajes indicando si el número es primo o no.  

**Uso:**  
```python
main()
```

---

### 2. División Controlada  
**Método:** `dividir(a, b)`  
**Descripción:**  
- Realiza la división de dos números.  
- Maneja el error de división por cero devolviendo 0.  

**Uso:**  
```python
main()
```

---

### 3. Longitudes de Cadenas  
**Método:** `longitudes_cadenas(lista_cadenas)`  
**Descripción:**  
- Recibe una lista de cadenas y devuelve una lista con las longitudes de cada cadena.  
- Utiliza List Comprehension.  

**Uso:**  
```python
cadenas = ["Hola", "Python", "Mundo", "Programación"]
longitudes = longitudes_cadenas(cadenas)
print(longitudes)
```

---

### 4. Conversión Binario-Decimal  
**Métodos:**  
- `binario_a_decimal(binario)`  
- `decimal_a_binario(decimal)`  

**Descripción:**  
- Convierte una cadena binaria a decimal y viceversa.  

**Uso:**  
```python
cadena_binaria = "1101"
print(binario_a_decimal(cadena_binaria))

numero_decimal = 13
print(decimal_a_binario(numero_decimal))
```

---

### 5. Reverso de Cadena  
**Método:** `reverso_cadena(cadena)`  
**Descripción:**  
- Invierte una cadena de texto utilizando listas y el método `reverse()`.  

**Uso:**  
```python
cadena = "Hola Mundo"
print(reverso_cadena(cadena))
```

---

### 6. Mayor en Cada Posición  
**Método:** `mayor_en_cada_posicion(lista1, lista2)`  
**Descripción:**  
- Recibe dos listas y devuelve una nueva lista con el mayor valor en cada posición.  
- Utiliza `map` y una función lambda.  

**Uso:**  
```python
lista1 = [3, 2, 5]
lista2 = [4, 1, 1]
print(mayor_en_cada_posicion(lista1, lista2))
```

---

### 7. Conjetura de Collatz  
**Método:** `collatz_sequence(n, memo)`  
**Descripción:**  
- Comprueba la conjetura de Collatz para números del 1 al 100.  
- Almacena los recorridos en una lista de listas y muestra el número con el recorrido más largo.  

**Uso:**  
```python
main()
```

---

### 8. Gestión de Frutería  
**Métodos:**  
- `añadir_articulo_tienda()`  
- `mostrar_tienda()`  
- `crear_cesta()`  
- `añadir_articulo_cesta()`  
- `calcular_total_cesta()`  

**Descripción:**  
- Programa interactivo que simula una frutería con opciones para añadir artículos, mostrar la tienda, gestionar una cesta de compra y calcular el total.  

**Uso:**  
```python
Ejecutar el programa y seguir las opciones del menú.
```

---

### 9. Diccionario de Traducción  
**Métodos:**  
- `añadir_palabras()`  
- `traducir_frase()`  

**Descripción:**  
- Permite añadir palabras a un diccionario español-inglés y traducir frases palabra por palabra.  

**Uso:**  
```python
Ejecutar el programa y seguir las opciones del menú.
```

---

## Estilo de Codificación  
- Indentación de 4 espacios.  
- Líneas limitadas a 79 caracteres.  
- Uso de espacios alrededor de operadores y después de comas.  
- Nombres descriptivos para funciones y variables.  

--- 

## Notas  
Todos los ejercicios están implementados siguiendo las mejores prácticas de Python y están listos para ejecutarse en cualquier entorno compatible con Python 3.