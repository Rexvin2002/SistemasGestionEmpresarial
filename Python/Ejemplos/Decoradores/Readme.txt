# Ejemplo de Decoradores en Python

## Autor: Kevin Gómez Valderas  
## Curso: 2º DAM  

---

## Descripción  
Este ejemplo muestra cómo implementar y utilizar decoradores en Python, una característica poderosa que permite modificar o extender el comportamiento de funciones sin cambiar su código fuente.

---

## Código Explicado

### Estructura del Decorador
```python
def funcion_a(funcion_b):
    def funcion_c():
        print("Antes de la ejecución de la función a decorar")
        funcion_b()
        print("Después de la ejecución de la función a decorar")
    return funcion_c
```

- **`funcion_a`**: Es el decorador que recibe como parámetro la función a decorar (`funcion_b`).
- **`funcion_c`**: Es la función envoltorio (wrapper) que:
  1. Ejecuta código antes de llamar a la función original.
  2. Llama a la función original (`funcion_b`).
  3. Ejecuta código después de llamar a la función original.
- **`return funcion_c`**: Devuelve la función envoltorio para reemplazar a la función original.

---

### Uso del Decorador
```python
@funcion_a
def saludar():
    print("Hola mundo!!")

saludar()
```

- **`@funcion_a`**: Sintaxis para aplicar el decorador `funcion_a` a la función `saludar`.
- Cuando se llama a `saludar()`, en realidad se ejecuta la versión decorada (`funcion_c`).

---

## Salida Esperada
```
Antes de la ejecución de la función a decorar
Hola mundo!!
Después de la ejecución de la función a decorar
```

---

## Conceptos Clave
1. **Decoradores**: Funciones que modifican el comportamiento de otras funciones.
2. **Función envoltorio**: Contiene la lógica adicional y llama a la función original.
3. **Sintaxis `@`**: Forma concisa de aplicar decoradores.

---

## Aplicaciones Comunes
- Validación de parámetros
- Medición del tiempo de ejecución
- Registro de logs
- Control de acceso

Este ejemplo demuestra el patrón básico para crear decoradores en Python, que puede extenderse para diversas funcionalidades.