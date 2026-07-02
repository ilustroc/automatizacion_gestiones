# Automatizacion de gestiones de cobranza

Proyecto academico para el curso Lenguajes de Programacion. Automatiza el proceso de descarga, limpieza, homologacion, validacion, carga y reporte de gestiones de cobranza usando Python y PostgreSQL/Supabase.

## Problema que resuelve

En una operacion de cobranzas como ESCALL PERU, las gestiones pueden prepararse manualmente antes de reportarse. Esto genera demoras, duplicados, errores de digitacion, tipificaciones no estandarizadas y poca trazabilidad.

El sistema centraliza el flujo en la base de datos: registra cargas, procesa gestiones, evita duplicados, guarda logs y consulta reportes desde `vw_resumen_gestiones`.

## Paradigma usado

El proyecto usa programacion orientada a objetos. Las responsabilidades se separan en clases:

- `Gestion`
- `DescargadorService`
- `LimpiadorService`
- `HomologadorService`
- `ValidadorService`
- `GestionRepository`
- `ReporteService`
- `NotificacionService`

Tambien se aplica organizacion modular por capas: `models`, `services`, `repositories`, `utils`, `docs` y `tests`.

## Arquitectura

```text
Supabase/PostgreSQL
-> repositories
-> services
-> models/utils
-> reportes/logs
-> usuario analista
```

El CSV ya no es el flujo principal. Puede mantenerse como respaldo academico o archivo de ejemplo, pero la ejecucion principal usa PostgreSQL/Supabase.

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuracion del .env

Crear un archivo `.env` en la raiz del proyecto tomando como base `.env.example`:

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

No subir credenciales reales a GitHub.

`DATABASE_SOURCE_QUERY` permite definir la consulta que obtiene las gestiones de origen. En una fase futura puede reemplazarse por un Stored Procedure.

## Ejecucion del sistema

```bash
python run.py
```

Flujo principal:

1. Cargar configuracion desde `.env`.
2. Conectarse a PostgreSQL/Supabase.
3. Crear registro en `cargas_gestiones`.
4. Obtener gestiones desde base de datos.
5. Limpiar campos.
6. Homologar status y tipificacion.
7. Validar campos obligatorios.
8. Generar `clave_unica`.
9. Insertar registros no duplicados en `gestiones`.
10. Actualizar la carga.
11. Registrar logs en `logs_proceso`.
12. Mostrar resumen desde `vw_resumen_gestiones`.

## Ejecucion de pruebas

```bash
python -m pytest -q
```

Las pruebas no dependen de Supabase real. La insercion en base de datos se simula con mocks/fakes.

## Base de datos

El script SQL se encuentra en:

```text
docs/schema.sql
```

Tablas principales:

- `empresas`
- `usuarios`
- `carteras`
- `cargas_gestiones`
- `gestiones`
- `reportes`
- `destinatarios_reportes`
- `envios_reportes`
- `logs_proceso`
- `vw_resumen_gestiones`

## Evidencias para presentacion

Capturas recomendadas:

- ejecucion de `python run.py`
- configuracion `.env` sin mostrar contrasena
- tablas creadas en Supabase
- registros en `cargas_gestiones`
- registros en `gestiones`
- logs en `logs_proceso`
- consulta de `vw_resumen_gestiones`
- pruebas aprobadas con `python -m pytest -q`

## Documentacion

- `docs/paradigma_programacion.md`
- `docs/contexto_empresarial.md`
- `docs/objetivos.md`
- `docs/proceso_automatizar.md`
- `docs/modelo_logico.md`
- `docs/modelo_fisico_base_datos.md`
- `docs/codigo_fuente.md`
- `docs/presentacion_automatizacion.md`
- `docs/conclusiones_recomendaciones.md`
- `docs/guia_exposicion.md`
- `docs/schema.sql`

