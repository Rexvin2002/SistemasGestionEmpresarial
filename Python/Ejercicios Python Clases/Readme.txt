# Proyectos de Programación - Kevin Gómez Valderas (2ºDAM)

Este repositorio contiene tres proyectos de programación implementados en Python:

## 1. Manejo de Fracciones (`Fraction`)

Implementación de una clase para operaciones básicas con fracciones.

### Características:
- Simplificación automática de fracciones
- Suma de fracciones
- Comparación de fracciones
- Manejo de signos
- Interfaz de usuario interactiva

### Uso:
```python
# Crear fracciones
f1 = Fraction(1, 2)
f2 = Fraction(3, 4)

# Operaciones
suma = f1 + f2
print(f"Suma: {suma}")
print(f"¿Son iguales?: {f1 == f2}")
```

## 2. Figuras Geométricas (`GeometricFigure`)

Sistema de herencia para cálculo de áreas de figuras geométricas.

### Clases implementadas:
- `GeometricFigure`: Clase base abstracta
- `RightTriangle`: Triángulo rectángulo (calcula hipotenusa y área)
- `Rectangle`: Rectángulo (calcula área)
- `FigureList`: Gestor de colección de figuras

### Funcionalidades:
- Cálculo de áreas
- Conteo de figuras por tipo
- Suma total de áreas

## 3. Juego Quixo

Implementación del juego de mesa Quixo con IA básica.

### Reglas del juego:
- Tablero 5x5
- Turnos alternados entre jugador y IA
- Movimiento de fichas desde los bordes
- Gana quien alinea 5 fichas iguales

### Características:
- Interfaz en español
- IA con tiempos de "reflexión" simulados
- Validación de movimientos
- Detección automática de ganador

### Cómo jugar:
1. Elegir símbolo (X/O)
2. Seleccionar posición inicial (bordes del tablero)
3. Elegir dirección de movimiento
4. Intentar alinear 5 fichas

## Requisitos
- Python 3.x
- Módulos estándar: `random`, `time`

## Ejecución
Cada proyecto puede ejecutarse directamente:
```bash
python fraction_project.py
python geometric_figures.py
python quixo_game.py
```

## Autor
Kevin Gómez Valderas  
Estudiante de 2º Desarrollo de Aplicaciones Multiplataforma (DAM)