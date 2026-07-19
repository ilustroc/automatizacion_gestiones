# Requisitos del proyecto final

## Funcionales

1. Mantener conexiones independientes a ESCALL y MySQL/MariaDB local.
2. Diagnosticar tabla, columnas, SP, versiones y estructuras sin modificar datos.
3. Descargar mediante `sp_descargar_gestiones_rango` con fechas parametrizadas.
4. Limpiar, homologar, validar y generar SHA-256.
5. Insertar por lotes y evitar duplicados.
6. Administrar controles manuales, pendientes y automáticos.
7. Ejecutar la última hora cerrada de forma idempotente.
8. Generar reportes para supervisor, Impulse y gerencia desde la base local.
9. Exportar Excel, enviar HTML/adjuntos y registrar intentos.
10. Ofrecer CLI, Tkinter y jobs programables.

## No funcionales

1. Python 3.11+, incluido 3.13.
2. MySQL/MariaDB y cPanel/phpMyAdmin.
3. Credenciales únicamente en `.env`, contraseñas entre comillas dobles.
4. Consultas parametrizadas y privilegios mínimos en ESCALL.
5. Transacciones y rollback local.
6. POO y arquitectura por capas.
7. Pruebas sin conexiones o correos reales.
8. CSV no operativo, conservado solo como ejemplo.
