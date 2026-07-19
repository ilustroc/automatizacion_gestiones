# Nota histórica de implementación

Este nombre de archivo se conserva para no borrar documentación de entregas anteriores. Supabase/PostgreSQL ya no forma parte de la arquitectura final.

La implementación vigente usa:

- MySQL/MariaDB de ESCALL como origen de solo lectura;
- MySQL/MariaDB local como destino del proyecto;
- `SOURCE_DB_*` y `TARGET_DB_*` en `.env`;
- scripts separados en `docs/sql`.

Consultar `README.md` e `instalacion_bases_datos.md` para la instalación actual.
