# Sistema de Gestión de Vehículos en Taller

## Autor: Kevin Gómez Valderas  
## Curso: 2º DAM  

---

## Descripción  
Este proyecto implementa un sistema de gestión de vehículos para talleres mecánicos utilizando programación orientada a objetos en Python. Incluye diferentes tipos de vehículos y operaciones de taller.

---

## Estructura de Clases

### 1. Clase Base: `Vehiculo`
- **Atributos**:
  - `numeroruedas`: Número de ruedas del vehículo
- **Métodos**:
  - `mostrar()`: Muestra información básica del vehículo

### 2. Clase Derivada: `Coche`
- **Hereda de**: `Vehiculo` (4 ruedas por defecto)
- **Atributos**:
  - `_matricula`: Matrícula del coche (privado)
- **Métodos**:
  - `matricular(nmatricula)`: Asigna una nueva matrícula

### 3. Clase Derivada: `Bicicleta`
- **Hereda de**: `Vehiculo` (2 ruedas por defecto)
- **Atributos**:
  - `ruedashinchadas`: Estado de las ruedas
- **Métodos**:
  - `hincharrueda()`: Cambia el estado de las ruedas a hinchadas
  - `mostrar()`: Sobrescribe el método para mostrar estado específico

### 4. Clase: `Taller`
- **Atributos**:
  - `vehiculos`: Lista de vehículos en el taller
- **Métodos**:
  - `nuevocoche(matricula)`: Añade un coche al taller
  - `nuevabici()`: Añade una bicicleta al taller
  - `hincharruedas()`: Hincha ruedas de todas las bicicletas
  - `mostrartaller()`: Muestra información de todos los vehículos
  - `metodotonto()`: Método de ejemplo sin funcionalidad

---

## Ejemplo de Uso

```python
t = Taller()
t.nuevocoche("AAAAA")  # Añade coche con matrícula AAAAA
t.nuevabici()         # Añade bicicleta
t.nuevabici()         # Añade otra bicicleta
t.nuevocoche("BBBB")  # Añade coche con matrícula BBBB

t.mostrartaller()     # Muestra estado actual
t.hincharruedas()     # Hincha ruedas de bicicletas
t.mostrartaller()     # Muestra estado después de hinchar
t.metodotonto()       # Ejecuta método adicional
```

---

## Salida Esperada

```
Vehiculo con 4 ruedas
Bicicleta con las ruedas deshinchadas
Bicicleta con las ruedas deshinchadas
Vehiculo con 4 ruedas

[Después de hinchar ruedas]
Vehiculo con 4 ruedas
Bicicleta con las ruedas hinchadas
Bicicleta con las ruedas hinchadas
Vehiculo con 4 ruedas

Vaya Tonteria
```

---

## Diagrama de Clases (Pseudocódigo)

```
Vehiculo (base)
├── Coche
│   ├── matricular()
└── Bicicleta
    ├── hincharrueda()

Taller (contiene Vehiculos)
├── gestión de vehículos
└── operaciones de taller
```

---

## Mejoras Futuras
1. Añadir más tipos de vehículos (motos, camiones)
2. Implementar sistema de reparaciones
3. Añadir historial de mantenimiento
4. Crear interfaz gráfica
5. Añadir persistencia de datos (guardar en archivo/BD)

Este sistema proporciona una base sólida para gestionar diferentes tipos de vehículos en un taller mecánico, con capacidad de extensión para nuevas funcionalidades.