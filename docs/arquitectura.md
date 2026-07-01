# Arquitectura

El proyecto usa una arquitectura sencilla por capas. La idea es separar responsabilidades sin crear una estructura dificil de explicar.

## Capas

### Models

Contiene las clases principales del sistema. En esta primera version se incluye la clase `Gestion`.

### Services

Contiene la logica de negocio:

- `LimpiadorService`: limpia datos operativos.
- `HomologadorService`: convierte status y tipificaciones a valores estandar.
- `ValidadorService`: valida columnas y elimina duplicados.
- `ReporteService`: genera el archivo Excel y el resumen del proceso.

### Repositories

Contiene una clase base para futura persistencia en PostgreSQL/Supabase. En esta version no se conecta a una base real.

### Utils

Contiene funciones pequenas reutilizables para texto, numeros y fechas.

## Decision sobre ILOCALIZADO

Cuando `ILOCALIZADO` aparece como status se homologa a `NO CONTACTO`, porque representa que no se logro contactar ni ubicar al cliente. Cuando aparece como tipificacion, se conserva como `ILOCALIZADO`.

