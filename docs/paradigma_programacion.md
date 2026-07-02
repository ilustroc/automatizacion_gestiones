# Paradigma de programacion

El proyecto usa principalmente el paradigma de programacion orientada a objetos.

## Justificacion

La programacion orientada a objetos permite representar el proceso de cobranza mediante clases con responsabilidades claras. Esto ayuda a explicar el sistema en una exposicion academica y facilita el mantenimiento del codigo.

## Conceptos aplicados

### Clases

Una clase define atributos y metodos. En el proyecto existen clases como `Gestion`, `LimpiadorService`, `HomologadorService`, `ValidadorService` y `GestionRepository`.

### Objetos

Un objeto es una instancia de una clase. Por ejemplo, durante la ejecucion se crean objetos como `limpiador`, `homologador`, `validador` y `gestion_repository`.

### Atributos

Los atributos guardan informacion. En `Gestion`, los atributos principales son `fecha_gestion`, `dni`, `telefono`, `status`, `tipificacion`, `observacion`, `fecha_pago`, `monto_pago`, `nombre` y `clave_unica`.

### Metodos

Los metodos representan acciones. Por ejemplo:

- `limpiar_dataframe()`
- `homologar_status()`
- `obtener_registros_validos()`
- `agregar_clave_unica()`
- `insertar_gestiones()`

## Organizacion modular por capas

Ademas de POO, el proyecto se organiza por capas:

- `models`: entidades del dominio.
- `services`: logica de negocio.
- `repositories`: acceso a PostgreSQL/Supabase.
- `utils`: funciones reutilizables.
- `tests`: pruebas unitarias.
- `docs`: documentacion academica y tecnica.

## Patrones simples usados

- Service Layer: separa la logica de limpieza, homologacion, validacion y reportes.
- Repository: separa el acceso a base de datos del resto del sistema.

No se usan patrones avanzados innecesarios, porque el objetivo es mantener un proyecto claro, profesional y facil de explicar.

