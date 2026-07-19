# Diccionario de datos principal

## `control_descargas_gestiones`

| Campo | Tipo | Descripción |
|---|---|---|
| `id_control` | BIGINT PK | Identificador de ejecución |
| `fecha_desde` | DATETIME | Límite inicial inclusivo |
| `fecha_hasta` | DATETIME | Límite final exclusivo |
| `estado` | ENUM | PENDIENTE, EN_PROCESO, FINALIZADO o ERROR |
| `tipo_descarga` | ENUM | MANUAL o AUTOMATICA |
| `registros_*` | INT | Origen, insertados, duplicados e inválidos |
| `mensaje_error` | TEXT | Error comprensible de la ejecución |
| `fecha_inicio_proceso` | DATETIME | Inicio real |
| `fecha_fin_proceso` | DATETIME | Fin real |

## `gestiones_procesadas`

| Campo | Tipo | Descripción |
|---|---|---|
| `id_procesado` | BIGINT PK | Identificador local |
| `id_gestion_origen` | BIGINT | Identificador de ESCALL |
| `fecha_gestion` | DATETIME | Fecha y hora normalizada |
| `dni` | VARCHAR(20) | Documento conservado como texto |
| `telefono` | VARCHAR(30) | Teléfono limpio o NULL |
| `status_original` | VARCHAR(100) | Valor recibido |
| `tipificacion_original` | VARCHAR(150) | Valor recibido |
| `status_homologado` | VARCHAR(50) | DIRECTO, INDIRECTO, NO CONTACTO o SIN GESTIÓN |
| `tipificacion_homologada` | VARCHAR(150) | Regla estandarizada |
| `fecha_pago` | DATE | Promesa o pago, si corresponde |
| `monto_pago` | DECIMAL(14,2) | Monto normalizado |
| `nombre_asesor` | VARCHAR(150) | Asesor asociado |
| `clave_unica` | CHAR(64) UNIQUE | SHA-256 hexadecimal |
| `id_control_descarga` | BIGINT FK | Ejecución que insertó la fila |

Las definiciones completas están en `docs/sql/02_target_local_schema.sql`.
