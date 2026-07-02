# Modelo base de datos

La base de datos objetivo es PostgreSQL en Supabase, usando el schema `public`.

## Tablas

- `empresas`: empresas o clientes externos.
- `usuarios`: usuarios internos.
- `carteras`: carteras asociadas a empresas.
- `cargas_gestiones`: ejecuciones del proceso.
- `gestiones`: tabla central con gestiones limpias.
- `reportes`: reportes generados.
- `destinatarios_reportes`: destinatarios de reportes.
- `envios_reportes`: intentos de envio.
- `logs_proceso`: eventos del sistema.
- `vw_resumen_gestiones`: vista de resumen operativo.

## Tabla central

La tabla `gestiones` contiene:

- `id_gestion`
- `id_carga`
- `id_cartera`
- `id_usuario`
- `fecha_gestion`
- `dni`
- `telefono`
- `status`
- `tipificacion`
- `observacion`
- `fecha_pago`
- `monto_pago`
- `nombre`
- `clave_unica`
- `creado_en`

## Control de duplicados

La columna `clave_unica` se forma con:

```text
dni|telefono|fecha_gestion|status|tipificacion
```

La insercion usa `ON CONFLICT (clave_unica) DO NOTHING` para evitar duplicados.

