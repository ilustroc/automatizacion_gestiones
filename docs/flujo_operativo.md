# Flujo operativo

## Entrada principal

La entrada principal es PostgreSQL/Supabase. El sistema puede usar:

- una consulta SQL configurada en `DATABASE_SOURCE_QUERY`
- un futuro Stored Procedure configurado como mejora posterior

## Procesamiento

1. `DescargadorService` obtiene registros desde la base de datos.
2. `ValidadorService` valida columnas requeridas.
3. `LimpiadorService` limpia campos.
4. `HomologadorService` estandariza status y tipificacion.
5. `ValidadorService` descarta registros sin obligatorios.
6. `ValidadorService` elimina duplicados del lote.
7. `ValidadorService` genera `clave_unica`.
8. `GestionRepository` inserta en `gestiones`.
9. `CargaGestionRepository` actualiza la carga.
10. `LogProcesoRepository` registra eventos.
11. `ReporteService` consulta `vw_resumen_gestiones`.

## Salida principal

La salida principal queda en base de datos:

- registros insertados en `gestiones`
- ejecucion registrada en `cargas_gestiones`
- eventos registrados en `logs_proceso`
- resumen consultado desde `vw_resumen_gestiones`

La exportacion a Excel queda como opcion auxiliar, no obligatoria.

