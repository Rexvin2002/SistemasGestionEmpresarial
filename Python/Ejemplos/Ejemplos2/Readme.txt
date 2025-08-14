# Implementación de Clases Fracción y Fracción Mixta en Python

## Autor: Kevin Gómez Valderas  
## Curso: 2º DAM  

---

## Descripción  
Este proyecto implementa dos clases en Python para trabajar con fracciones:
1. `Fraccion`: Representa fracciones simples
2. `FraccionEnt`: Extiende `Fraccion` para representar fracciones mixtas (con parte entera)

---

## Clase Fraccion

### Atributos
- `numerador`: Parte superior de la fracción
- `denominador`: Parte inferior de la fracción (no puede ser cero)

### Métodos

#### `__init__(self, num, den)`
Constructor que inicializa la fracción.
- Valida que el denominador no sea cero (lanza `ZeroDivisionError`)
- Convierte a forma irreducible (no implementado completamente en el código mostrado)

#### `__repr__(self)`
Representación de la fracción como string en formato "numerador/denominador"

#### `__eq__(self, fraccionb)`
Compara si dos fracciones son iguales (mismo numerador y denominador)

---

## Clase FraccionEnt (Hereda de Fraccion)

### Atributos adicionales
- `pentera`: Parte entera de la fracción mixta

### Métodos
Hereda todos los métodos de `Fraccion` y añade:
- `__init__(self, num, den, ent)`: Constructor que inicializa la fracción mixta

---

## Ejemplo de Uso

```python
# Crear fracciones simples
x = Fraccion(1, 2)
x1 = Fraccion(1, 2)

# Crear fracción mixta
y = FraccionEnt(1, 2, 3)

# Comparación
if x == y:
    print("Son iguales")
else:
    print("Son diferentes")  # Este se ejecutará

# Mostrar fracción
print(x)  # Salida: "1/2"
```

---

## Salida Esperada
```
Son diferentes
1/2
```

---

## Mejoras Pendientes
1. Implementar completamente la simplificación de fracciones en el constructor
2. Añadir operaciones aritméticas (suma, resta, etc.)
3. Implementar conversión entre fracción simple y mixta
4. Añadir validación para números negativos
5. Implementar `__str__` para representación alternativa

---

## Requisitos
- Python 3.x
- No se requieren librerías externas

Este código proporciona una base para trabajar con fracciones en Python que puede extenderse según necesidades específicas.