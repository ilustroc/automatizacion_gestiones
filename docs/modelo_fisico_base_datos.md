# Modelo físico de base de datos

## Origen ESCALL

- Motor: MySQL/MariaDB en cPanel.
- Base: `escarperu_software`.
- Tabla existente: `gestiones`.
- Procedimiento de lectura: `sp_descargar_gestiones_rango`.
- Script: `docs/sql/01_source_escall_sp.sql`.

La aplicación verifica con `SHOW COLUMNS FROM gestiones` que existan `id`, `fecha_gestion`, `dni`, `telefono`, `status`, `tipificacion`, `observacion`, `fecha_pago`, `monto_pago`, `nombre`, `created_at` y `updated_at`. No ejecuta operaciones de escritura en este servidor.

## Destino local

- Motor: MySQL o MariaDB.
- Base: `automatizacion_gestiones`.
- Scripts: `docs/sql/02_target_local_schema.sql` y `03_target_local_views.sql`.

| Objeto | Propósito |
|---|---|
| `empresas` | Empresas relacionadas con carteras y usuarios |
| `usuarios` | Usuarios o responsables locales |
| `carteras` | Carteras de cobranza |
| `control_descargas_gestiones` | Rango, estado, contadores y error de cada ejecución |
| `cargas_gestiones` | Historial complementario de cargas |
| `gestiones_procesadas` | Datos limpios y homologados provenientes de ESCALL |
| `reportes` | Archivos y periodos generados |
| `destinatarios_reportes` | Destinos configurables por tipo |
| `envios_reportes` | Resultado de cada intento SMTP |
| `logs_proceso` | Eventos INFO, ADVERTENCIA y ERROR |

`gestiones_procesadas.clave_unica` es `CHAR(64)` y tiene índice único. Contiene el SHA-256 de los campos funcionales, evitando límites de longitud del índice y garantizando idempotencia.

## Vistas

- `vw_control_descargas_pendientes`: controles por ejecutar.
- `vw_alerta_promesas_pago`: promesas vencidas, de hoy, mañana y próximas.
- `vw_reporte_impulse_gestiones`: detalle operativo local.
- `vw_reporte_gerencia_asesores_dia`: indicadores por fecha y asesor.
- `vw_ranking_gerencia_asesores_dia`: ranking cuando el motor admite funciones de ventana.

Las relaciones usan InnoDB y claves foráneas locales. No existe una clave foránea entre servidores; `id_gestion_origen` conserva la trazabilidad hacia ESCALL.
