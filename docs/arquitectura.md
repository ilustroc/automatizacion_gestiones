# Arquitectura

El proyecto usa una arquitectura modular por capas. La fuente y destino principal es PostgreSQL/Supabase.

## Capas

### Models

Contiene entidades del dominio. La clase principal es `Gestion`.

### Services

Contiene la logica de negocio:

- `DescargadorService`: obtiene registros desde base de datos o futuro Stored Procedure.
- `LimpiadorService`: limpia campos operativos.
- `HomologadorService`: estandariza status y tipificaciones.
- `ValidadorService`: valida obligatorios, elimina duplicados y genera `clave_unica`.
- `ReporteService`: consulta y formatea el resumen desde `vw_resumen_gestiones`.
- `NotificacionService`: deja preparado el envio futuro de reportes.

### Repositories

Contiene el acceso a PostgreSQL/Supabase:

- `EmpresaRepository`
- `UsuarioRepository`
- `CarteraRepository`
- `CargaGestionRepository`
- `GestionRepository`
- `ReporteRepository`
- `LogProcesoRepository`

### Utils

Funciones reutilizables para texto y fechas.

## Flujo

1. `run.py` inicia el proceso.
2. Se carga `.env`.
3. Se conecta a Supabase.
4. Se crea una carga en `cargas_gestiones`.
5. Se obtienen gestiones desde una consulta SQL.
6. Se limpian, homologan y validan los datos.
7. Se insertan gestiones no duplicadas.
8. Se registran logs.
9. Se muestra el resumen desde `vw_resumen_gestiones`.

## Nota sobre CSV

El CSV queda solo como respaldo academico o ejemplo. No es el flujo principal.

