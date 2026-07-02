# Presentacion de la automatizacion

## Evidencias esperadas

Para la presentacion se recomienda preparar capturas de:

1. Ejecucion del sistema con `python run.py`.
2. Archivo `.env` configurado sin mostrar contrasenas.
3. Conexion a Supabase activa.
4. Tablas creadas en Supabase:
   - empresas
   - usuarios
   - carteras
   - cargas_gestiones
   - gestiones
   - reportes
   - destinatarios_reportes
   - envios_reportes
   - logs_proceso
5. Registros procesados en `gestiones`.
6. Registro creado en `cargas_gestiones`.
7. Logs generados en `logs_proceso`.
8. Consulta de `vw_resumen_gestiones`.
9. Pruebas unitarias aprobadas con `python -m pytest -q`.

## Mensaje clave

La automatizacion reduce tareas manuales, evita duplicados, mejora la trazabilidad y permite consultar reportes desde la base de datos.

