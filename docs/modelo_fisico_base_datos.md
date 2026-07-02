# Modelo fisico de base de datos

La base fisica esta implementada en PostgreSQL/Supabase dentro del schema `public`.

## Tablas

### empresas

Registra empresas o clientes externos.

### usuarios

Registra usuarios internos con roles como administrador, supervisor, analista o asesor.

### carteras

Agrupa carteras o campanas asociadas a una empresa.

### cargas_gestiones

Controla cada ejecucion del proceso. Guarda estado, periodo, origen, registros descargados, insertados y duplicados.

### gestiones

Tabla central del sistema. Guarda gestiones limpias y homologadas.

Campos principales:

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

### reportes

Registra reportes generados por tipo y periodo.

### destinatarios_reportes

Guarda destinatarios que recibiran reportes.

### envios_reportes

Registra intentos de envio, estado y errores.

### logs_proceso

Guarda eventos y errores asociados a una carga.

### vw_resumen_gestiones

Vista que resume gestiones por fecha, status y tipificacion. Es la fuente principal del reporte en consola.

## Relaciones principales

- `empresas` se relaciona con `carteras`.
- `carteras` se relaciona con `gestiones`.
- `usuarios` se relaciona con `gestiones`.
- `cargas_gestiones` se relaciona con `gestiones` y `logs_proceso`.
- `reportes` se relaciona con `envios_reportes`.
- `destinatarios_reportes` se relaciona con `envios_reportes`.

