# Instalación de bases de datos

## 1. Servidor ESCALL

1. Ingresar a cPanel y abrir phpMyAdmin.
2. Seleccionar la base `escarperu_software`.
3. Abrir la pestaña **SQL**.
4. Pegar `docs/sql/01_source_escall_sp.sql` y ejecutar.
5. Ejecutar el `CALL` de prueba incluido.
6. Confirmar que el usuario creador tenga `CREATE ROUTINE`, `ALTER ROUTINE`, `EXECUTE` y `SELECT`.
7. Otorgar al usuario remoto de la aplicación únicamente `SELECT`, `EXECUTE` y `SHOW VIEW`.
8. Autorizar la IP del equipo en **Remote MySQL** de cPanel.

## 2. Servidor local

1. Iniciar MySQL/MariaDB.
2. Ejecutar `docs/sql/02_target_local_schema.sql`.
3. Ejecutar `SELECT VERSION();`.
4. Ejecutar `docs/sql/03_target_local_views.sql`.
5. Si la versión no admite `DENSE_RANK`, omitir únicamente `vw_ranking_gerencia_asesores_dia`; Python genera el ranking.

## 3. Aplicación

1. Crear `.env` con dos grupos de credenciales independientes.
2. Escribir las contraseñas entre comillas dobles.
3. Instalar `requirements.txt`.
4. Ejecutar `python run.py --modo diagnostico`.

El diagnóstico no inserta datos. Una conexión solo puede declararse operativa cuando este comando la haya probado con credenciales y permisos reales.
