# Flujo operativo

Este documento complementa `proceso_automatizar.md`.

1. Registrar un rango válido o seleccionar un pendiente.
2. Conectar el destino y marcar el control `EN_PROCESO`.
3. Conectar ESCALL y ejecutar el Stored Procedure parametrizado.
4. Limpiar, homologar y validar.
5. Generar SHA-256 y descartar duplicados del lote.
6. Insertar por lotes en `gestiones_procesadas`.
7. Confirmar la transacción local y finalizar el control.
8. Consultar vistas locales para reportes.
9. Generar HTML/Excel y, con confirmación, enviar por SMTP.
10. Registrar logs, reportes y envíos.

Si ocurre un error, se revierte la transacción de destino y el control queda en `ERROR`. ESCALL permanece sin modificaciones.
