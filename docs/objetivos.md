# Objetivos

## Objetivo general

Automatizar el proceso de descarga, limpieza, homologacion, validacion, carga y reporte de gestiones de cobranza usando Python y PostgreSQL/Supabase.

## Objetivos especificos

1. Conectar el sistema Python a la base de datos PostgreSQL/Supabase mediante variables de entorno.
2. Registrar cada ejecucion en la tabla `cargas_gestiones`.
3. Obtener gestiones desde una consulta SQL o un futuro Stored Procedure.
4. Limpiar campos operativos como DNI, telefono, observacion, nombre, fechas y montos.
5. Homologar status y tipificaciones para obtener valores consistentes.
6. Validar campos obligatorios antes de insertar datos.
7. Generar una `clave_unica` para evitar duplicados.
8. Insertar en la tabla `gestiones` solo registros validos y no duplicados.
9. Registrar eventos y errores en `logs_proceso`.
10. Consultar reportes desde la vista `vw_resumen_gestiones`.

