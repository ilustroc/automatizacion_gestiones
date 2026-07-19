# Automatización de gestiones de cobranza

Proyecto académico del curso Lenguajes de Programación. Automatiza la descarga, limpieza, homologación, validación, deduplicación, almacenamiento y reporte de gestiones de cobranza de ESCALL PERÚ.

## Arquitectura final

El sistema trabaja con dos bases MySQL/MariaDB independientes:

1. **Origen ESCALL:** base `escarperu_software` alojada en cPanel. La aplicación solo ejecuta `sp_descargar_gestiones_rango` y nunca inserta, actualiza ni elimina datos.
2. **Destino local:** base `automatizacion_gestiones`. Guarda controles, gestiones procesadas, logs, reportes y envíos.

```text
ESCALL / gestiones
-> Stored Procedure de lectura
-> Python
-> limpieza -> homologación -> validación -> SHA-256
-> MySQL local / gestiones_procesadas
-> vistas -> HTML/Excel -> SMTP
-> logs y auditoría
```

El CSV de la primera entrega se conserva en `data/examples/gestiones.csv` únicamente como evidencia académica. No participa en el flujo principal.

## Paradigma y capas

Se usa Programación Orientada a Objetos. Los objetos encapsulan configuración, conexiones, modelos, repositorios y servicios. La solución aplica arquitectura por capas:

- `app/models`: entidades con `dataclasses` y tipos.
- `app/repositories`: acceso parametrizado a origen y destino.
- `app/services`: procesamiento, diagnóstico, reportes y notificación.
- `app/ui`: interfaz Tkinter para registrar y ejecutar rangos.
- `jobs`: descarga horaria y envío programado de reportes.
- `docs`: SQL, informe, guías y diagramas.
- `tests`: pruebas con fakes y mocks, sin bases ni correos reales.

## Requisitos

- Windows 10/11 o servidor Linux/cPanel.
- Python 3.11 o superior, compatible con Python 3.13.
- MySQL o MariaDB local.
- Acceso remoto de lectura al MySQL de ESCALL.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Instalación SQL

En ESCALL, seleccionar `escarperu_software` en phpMyAdmin y ejecutar:

```text
docs/sql/01_source_escall_sp.sql
```

El usuario que crea el procedimiento necesita `SELECT`, `CREATE ROUTINE`, `ALTER ROUTINE` y `EXECUTE`. El usuario remoto de la aplicación solo necesita `SELECT`, `EXECUTE` y `SHOW VIEW`.

En MySQL/MariaDB local, ejecutar en orden:

```text
docs/sql/02_target_local_schema.sql
docs/sql/03_target_local_views.sql
```

La última vista usa `DENSE_RANK`, disponible en MySQL 8+ y MariaDB 10.2+. Si el motor es anterior, puede omitirse: Python calcula el ranking gerencial.

## Configuración

Crear `.env` a partir de `.env.example`. Todas las contraseñas deben ir entre comillas dobles, sin espacios alrededor de `=`:

```dotenv
SOURCE_DB_PASSWORD="contraseña_origen_con_simbolos"
TARGET_DB_PASSWORD="contraseña_local"
SMTP_PASSWORD="contraseña_del_correo"
```

`python-dotenv` retira las comillas y conserva caracteres como `&`, `#`, `?`, `{}`, `[]`, `+`, `-`, `@` y `%`. El archivo `.env` está excluido por `.gitignore`.

Los grupos de variables son:

- `SOURCE_DB_*`: servidor ESCALL.
- `TARGET_DB_*`: servidor local.
- `SMTP_*`: servidor y remitente completo.
- `MAIL_*`: gerencia, supervisor e Impulse.
- `BATCH_SIZE`, `EXPORTAR_EXCEL`, `ENVIAR_CORREOS`, `APP_TIMEZONE`.

## Diagnóstico

```powershell
python run.py --modo diagnostico
```

Comprueba ambas conexiones, versiones, columnas de `gestiones`, Stored Procedure y tablas locales. Es de solo lectura y no muestra contraseñas. Si no hay credenciales o acceso, termina de forma controlada e indica qué configurar.

## Descargas

Rango de días. La fecha final se interpreta como día inclusivo; el ejemplo consulta desde `2026-07-01 00:00:00` hasta el límite exclusivo `2026-07-19 00:00:00`:

```powershell
python run.py --modo manual --fecha-inicio 2026-07-01 --fecha-fin 2026-07-18
```

Rango exacto de fecha y hora:

```powershell
python run.py --modo manual --fecha-desde "2026-07-18 08:00:00" --fecha-hasta "2026-07-18 09:00:00"
```

Procesar el control pendiente más antiguo:

```powershell
python run.py --modo pendiente
```

Procesar la última hora cerrada:

```powershell
python run.py --modo automatico
```

Abrir la interfaz:

```powershell
python run.py --interfaz
```

## Reportes

Generar Excel sin enviar correo:

```powershell
python run.py --reporte promesas --solo-generar
python run.py --reporte impulse --fecha-inicio 2026-07-18 --fecha-fin 2026-07-18 --solo-generar
python run.py --reporte gerencia --fecha-inicio 2026-07-01 --fecha-fin 2026-07-18 --solo-generar
python run.py --reporte todos --solo-generar
```

El envío real requiere `ENVIAR_CORREOS="true"` en `.env`, configuración SMTP válida y confirmación explícita:

```powershell
python run.py --reporte todos --enviar
```

El supervisor recibe promesas, Impulse recibe el detalle operativo y gerencia recibe productividad y ranking de asesores. Cada intento se registra en `envios_reportes`.

## Automatización horaria

Cron de cPanel para descargar cada hora cerrada:

```cron
0 * * * * cd /RUTA/automatizacion_gestiones && /usr/bin/python3 jobs/job_descarga_horaria.py >> logs/job_descarga_horaria.log 2>&1
```

Reportes programados:

```cron
15 8 * * * cd /RUTA/automatizacion_gestiones && /usr/bin/python3 jobs/job_envio_reportes.py --reporte promesas >> logs/job_reportes.log 2>&1
0 19 * * * cd /RUTA/automatizacion_gestiones && /usr/bin/python3 jobs/job_envio_reportes.py --reporte todos >> logs/job_reportes.log 2>&1
```

En Windows, crear tareas que ejecuten `python.exe` con cada script como argumento. La clave SHA-256 y el índice único hacen que repetir una hora no duplique gestiones.

## Pruebas

```powershell
python -m pytest -q
```

Las pruebas no abren conexiones reales ni envían correos.

## Evidencias sugeridas

- `SHOW COLUMNS FROM gestiones` y el procedimiento en ESCALL.
- Tablas y vistas de `automatizacion_gestiones`.
- Diagnóstico controlado.
- Descarga manual y contadores del control.
- Registros en `gestiones_procesadas` y hash de 64 caracteres.
- `logs_proceso`, `reportes` y `envios_reportes`.
- Los tres Excel y un correo de prueba autorizado.
- Resultado completo de `pytest`.

La guía de exposición está en `docs/guia_exposicion_final.md` y el informe consolidado en `docs/informe_final.md`.
