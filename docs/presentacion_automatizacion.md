# Presentación de la automatización

## Evidencias esperadas

1. **Origen ESCALL:** phpMyAdmin con base `escarperu_software`, tabla `gestiones`, columnas reales y `sp_descargar_gestiones_rango`.
2. **Destino local:** tablas creadas en `automatizacion_gestiones` y las cuatro vistas principales.
3. **Configuración segura:** `.env.example` con valores ficticios y `.gitignore` protegiendo `.env`.
4. **Diagnóstico:** consola mostrando ambas conexiones, versiones, columnas, SP y tablas, sin secretos.
5. **Ejecución:** rango manual y resumen de registros origen, insertados, duplicados e inválidos.
6. **Resultado local:** filas de `gestiones_procesadas` con originales, homologados y hash de 64 caracteres.
7. **Auditoría:** control finalizado y filas de `logs_proceso`.
8. **Promesas:** Excel/HTML con vencidas, hoy y mañana.
9. **Impulse:** resumen y detalle del periodo.
10. **Gerencia:** indicadores y ranking diario por asesor.
11. **Correo:** fila en `envios_reportes`; usar un envío real solo con autorización.
12. **Calidad:** salida completa de `python -m pytest -q`.

No capturar contraseñas, tokens, host privados completos ni datos personales innecesarios. Para una exposición, anonimizar DNI, teléfonos y correos si la información es real.

## Demostración breve

```powershell
python run.py --modo diagnostico
python run.py --modo manual --fecha-desde "2026-07-18 08:00:00" --fecha-hasta "2026-07-18 09:00:00"
python run.py --reporte todos --solo-generar
python -m pytest -q
```

La demostración debe distinguir claramente que la primera consulta lee ESCALL y que todo procesamiento y reporte posterior usa la base local.
