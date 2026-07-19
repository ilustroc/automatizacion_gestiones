# Objetivos

## Objetivo general

Automatizar la descarga desde ESCALL y el procesamiento, almacenamiento, control y reporte de gestiones de cobranza en una base local, reduciendo trabajo manual y mejorando calidad, oportunidad y trazabilidad.

## Objetivos específicos

1. Conectar de forma segura e independiente con la base origen ESCALL y la base destino local.
2. Descargar gestiones por rango exclusivo de fecha y hora mediante Stored Procedure, sin modificar ESCALL.
3. Limpiar DNI, teléfono, textos, fechas y montos sin perder ceros iniciales.
4. Homologar estados y tipificaciones mediante reglas configurables.
5. Validar campos obligatorios y descartar registros incompletos con contadores auditables.
6. Evitar duplicados con SHA-256 e índice único.
7. Registrar controles, transacciones, errores y logs en MySQL/MariaDB local.
8. Generar reportes de promesas, detalle para Impulse y productividad gerencial.
9. Permitir Excel, HTML, simulación y envío SMTP confirmado.
10. Ejecutar el proceso manualmente, por pendientes, con interfaz o mediante job horario.
