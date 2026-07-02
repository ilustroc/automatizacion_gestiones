# Proceso a automatizar

## Proceso actual

El proceso manual depende del analista. La informacion puede descargarse desde sistemas, consultas o archivos, luego se limpia manualmente, se revisan duplicados y se preparan reportes. Esto genera demoras, errores y poca trazabilidad.

## Proceso automatizado

El sistema automatizado usa PostgreSQL/Supabase como fuente y destino principal de informacion.

Flujo textual:

```text
Base de datos / SP
-> descarga
-> limpieza
-> homologacion
-> validacion
-> eliminacion de duplicados
-> carga en PostgreSQL/Supabase
-> reporte
-> logs
```

## Flujo implementado

1. Cargar configuracion desde `.env`.
2. Conectarse a PostgreSQL/Supabase.
3. Crear una carga en `cargas_gestiones` con estado `INICIADO`.
4. Obtener registros desde una consulta SQL definida.
5. Limpiar los campos operativos.
6. Homologar status y tipificacion.
7. Validar campos obligatorios.
8. Generar `clave_unica`.
9. Insertar registros en `gestiones` usando `ON CONFLICT DO NOTHING`.
10. Actualizar la carga con registros descargados, insertados y duplicados.
11. Registrar logs en `logs_proceso`.
12. Mostrar resumen consultado desde `vw_resumen_gestiones`.

