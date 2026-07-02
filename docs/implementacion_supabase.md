# Implementacion en Supabase

Supabase se usa como plataforma cloud porque trabaja sobre PostgreSQL y permite crear tablas, vistas y consultas desde SQL Editor.

## Datos de implementacion

- Proveedor: Supabase
- Motor: PostgreSQL
- Schema: `public`
- Script SQL: `docs/schema.sql`
- Conexion desde Python: variables de entorno en `.env`

## Variables de entorno

```text
DATABASE_HOST=
DATABASE_PORT=5432
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_SSLMODE=require
DATABASE_SOURCE_QUERY=
DATABASE_SOURCE_SP=
```

## Pasos

1. Crear proyecto en Supabase.
2. Abrir SQL Editor.
3. Ejecutar `docs/schema.sql`.
4. Revisar tablas en Table Editor.
5. Configurar `.env`.
6. Ejecutar `python run.py`.
7. Verificar registros en:
   - `cargas_gestiones`
   - `gestiones`
   - `logs_proceso`
   - `vw_resumen_gestiones`

## Seguridad

No se deben colocar credenciales reales en el codigo fuente ni subir el archivo `.env` a GitHub.

