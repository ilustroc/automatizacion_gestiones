# Codigo fuente

## Estructura de carpetas

### app/models

Contiene clases del dominio. La clase principal es `Gestion`.

### app/services

Contiene la logica del proceso:

- descarga desde base de datos
- limpieza
- homologacion
- validacion
- reportes
- preparacion de notificaciones

### app/repositories

Contiene el acceso a PostgreSQL/Supabase:

- conexion
- empresas
- usuarios
- carteras
- cargas
- gestiones
- reportes
- envios
- logs

### app/utils

Funciones reutilizables para texto, numeros y fechas.

### docs

Documentacion academica, tecnica y diagramas PlantUML.

### tests

Pruebas unitarias con pytest. Incluyen limpieza, homologacion, validacion, clave unica y simulacion de insercion en base de datos.

### run.py

Punto de entrada del sistema.

### requirements.txt

Dependencias del proyecto.

### .env.example

Plantilla de variables de entorno. No contiene credenciales reales.

