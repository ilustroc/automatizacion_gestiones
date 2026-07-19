# Proceso a automatizar

## Proceso anterior

1. Una persona extraía datos o trabajaba con un archivo intermedio.
2. Corregía manualmente DNI, teléfonos, fechas, montos y textos.
3. Interpretaba estados y tipificaciones con criterios no siempre uniformes.
4. Buscaba duplicados en hojas de cálculo.
5. Preparaba resúmenes y enviaba correos.
6. Los errores no siempre quedaban registrados.

## Proceso automatizado

```text
Base ESCALL / Stored Procedure
-> descarga parametrizada
-> limpieza
-> homologación
-> validación
-> SHA-256 y eliminación de duplicados
-> carga por lotes en MySQL/MariaDB local
-> vistas de reportes
-> HTML y Excel
-> SMTP
-> logs, controles y auditoría
```

1. CLI, Tkinter o job crea/selecciona un control con `fecha_desde` inclusiva y `fecha_hasta` exclusiva.
2. `SourceGestionRepository` ejecuta `CALL sp_descargar_gestiones_rango(%s, %s)` sobre ESCALL.
3. `LimpiadorService` normaliza los campos sin convertir el DNI a entero.
4. `HomologadorService` produce `DIRECTO`, `INDIRECTO`, `NO CONTACTO` o `SIN GESTIÓN`.
5. `ValidadorService` exige id de origen, fecha, DNI, status y tipificación.
6. La cadena `dni|telefono|fecha_gestion|status|tipificacion` se transforma en SHA-256 hexadecimal.
7. `GestionProcesadaRepository` usa `INSERT IGNORE` por lotes dentro de una transacción local.
8. El control registra origen, insertados, duplicados e inválidos.
9. Las vistas locales alimentan tres reportes; ESCALL ya no participa en esa etapa.
10. Los intentos de correo y los errores quedan auditados.

Ante una excepción se ejecuta `rollback`, el control pasa a `ERROR`, se guarda un mensaje comprensible y ambas conexiones se cierran.
