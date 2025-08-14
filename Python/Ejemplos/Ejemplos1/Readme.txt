# Ejemplos de Python

## Autor: Kevin Gómez Valderas  
## Curso: 2º DAM  

---

## Descripción  
Este documento contiene varios ejemplos que ilustran diferentes conceptos fundamentales de Python, incluyendo bucles, manejo de strings, listas, diccionarios, funciones lambda y manejo de excepciones.

---

## Ejemplos

### 1. Ejemplo1 - Secuencia de Fibonacci
```python
def ejemplo1():
    a, b = 0, 1
    while a < 100:
        print(a, end=",")
        a, b = b, a + b
```
**Descripción:**  
Muestra la secuencia de Fibonacci hasta que el valor sea menor que 100.  
**Salida:** `0,1,1,2,3,5,8,13,21,34,55,89,`

---

### 2. Ejemplo2 - Operaciones con Strings
```python
def ejemplo2():
    texto = "SGE es " + ("mi módulo " "favorito ")
    print(texto[0:3])  # 'SGE'
    print(texto[-3:])  # 'to '
    texto = 3 * texto  # Repite el texto 3 veces
```
**Descripción:**  
Demuestra concatenación, slicing y repetición de strings.

---

### 3. Ejemplo3 - Funciones con Parámetros por Defecto
```python
def frase(sujeto="SGE", verbo="es", predicado="mi modulo favorito"):
    print("{} {} {}".format(sujeto, verbo, predicado))

ejemplo3():
    frase(predicado="muy divertido")
```
**Salida:**  
`SGE es muy divertido`

---

### 4. Ejemplo4 - Operaciones con Listas
```python
def ejemplo4():
    squares = [1, 4, 9]
    squares.append(36)
    squares += [x**2 for x in range(10,13)]
    cubes = [[x, x**3] for x in range(6)]
```
**Descripción:**  
Muestra cómo manipular listas usando métodos, list comprehensions y listas anidadas.

---

### 5. Ejemplo5 - Diccionarios
```python
def ejemplo5():
    dic = {"uno": 1, "dos": 2}
    dic["cuatro"] = 4
    l = list(dic.keys())
    l.sort()
```
**Descripción:**  
Operaciones básicas con diccionarios: añadir elementos, obtener claves y ordenarlas.

---

### 6. Ejemplo6 - List Comprehension
```python
def listalong(lista):
    return [len(x) for x in lista]
```
**Uso:**  
Para una lista `["a", "ab", "abc"]` devuelve `[1, 2, 3]`.

---

### 7. Ejemplo7 - Manejo de Excepciones
```python
def soloimpar(n):
    if n % 2 == 0:
        raise Exception("Solo impares")

try:
    soloimpar(h)
except:
    print("El numero es par")
```
**Descripción:**  
Lanza una excepción si el número es par y la captura.

---

### 8. Ejemplo8 - Funciones Lambda
```python
def nfuncion(numero):
    return lambda x, y: (x - y) * 2 if x - y > numero else (x - y)

f = nfuncion(8)
print(f(10, 1))  # Devuelve 18 (9*2)
```
**Descripción:**  
Crea funciones lambda condicionales que modifican su comportamiento según un parámetro.

---

## Cómo Ejecutar
1. Copiar el código en un archivo Python (.py)
2. Ejecutar el archivo o llamar a las funciones individualmente
3. Para ejecutar todos los ejemplos, llamar a cada función `ejemploX()`

## Requisitos
- Python 3.x instalado
- No se requieren librerías adicionales

Este conjunto de ejemplos cubre conceptos esenciales de Python que son fundamentales para el desarrollo en este lenguaje.