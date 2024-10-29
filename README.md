# Juego de Adivinanzas

Un juego interactivo de adivinanzas desarrollado en Python utilizando Tkinter para la interfaz gráfica y MySQL para el almacenamiento de datos.

## Descripción

Este proyecto es un juego educativo que permite a los usuarios poner a prueba sus conocimientos en diferentes categorías mediante adivinanzas. El juego incluye un sistema de puntuación, seguimiento de progreso y perfiles de usuario.

![Interfases Principal del juego](/images/juego_adivinanza.png)


## Características Principales

- Interfaz gráfica intuitiva
- Múltiples categorías de adivinanzas
- Sistema de puntuación
- Perfiles de usuario
- Seguimiento de progreso
- Estadísticas detalladas
- Retroalimentación personalizada

## Estructura del Proyecto

```
proyecto/
│
├── main.py                 # Punto de entrada principal
├── database/
│   ├── mysql_connection.py # Gestión de conexiones a la base de datos
│   └── db.py              # Inicialización y gestión de la base de datos
│
└── gui/
    ├── inicio.py          # Pantalla de inicio
    ├── acerca_de.py       # Ventana "Acerca de"
    ├── adivinanza.py      # Interfaz del juego
    ├── perfil.py          # Gestión de perfiles
    └── seleccion_categoria.py  # Selección de categorías
```

## Requisitos

- Python 3.x
- MySQL
- Bibliotecas Python:
  - tkinter
  - mysql-connector-python

## Configuración de la Base de Datos

El juego utiliza MySQL para almacenar:
- Adivinanzas y sus categorías
- Progreso de los jugadores
- Estadísticas de juego

### Estructura de la Base de Datos

```sql
-- Tabla de Adivinanzas
CREATE TABLE Adivinanzas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    texto TEXT NOT NULL,
    respuesta TEXT NOT NULL,
    categoria TEXT NOT NULL,
    estado BOOLEAN DEFAULT FALSE
);

-- Tabla de Progreso
CREATE TABLE Progreso (
    nombre VARCHAR(255),
    categoria VARCHAR(255),
    puntos INT,
    intentos INT,
    adivinanzas_respondidas TEXT,
    PRIMARY KEY (nombre, categoria)
);
```

## Categorías de Adivinanzas

- Animales
- Comida
- Naturaleza
- Ciencia
- Deportes
- Geografía
- Cuentos y Fábulas
- Historia

## Sistema de Puntuación

- 2 puntos por respuesta correcta en el primer intento
- 1 punto por respuesta correcta en el segundo intento
- Máximo 2 intentos por adivinanza

## Características de la Interfaz

### Pantalla de Inicio
- Campo para ingresar nombre
- Botones para iniciar juego y ver perfil
- Menú con opciones adicionales

### Perfil del Jugador
- Estadísticas generales
- Progreso por categoría
- Índice de eficiencia
- Retroalimentación personalizada

### Ventana de Juego
- Visualización de adivinanzas
- Campo para respuestas
- Contador de intentos
- Puntuación actual

## Desarrollo

Para ejecutar el proyecto en modo desarrollo:

```bash
python main.py
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, asegúrate de:
1. Seguir las convenciones de código existentes
2. Documentar nuevas funcionalidades
3. Actualizar el README según sea necesario

## Licencia

Este proyecto está bajo la Licencia MIT.
