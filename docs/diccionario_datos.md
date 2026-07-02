# Diccionario de datos

## Tabla gestiones

| Campo | Tipo | Restriccion | Descripcion |
|---|---|---|---|
| id_gestion | BIGSERIAL | PK | Identificador unico de la gestion. |
| id_carga | BIGINT | FK, NOT NULL | Ejecucion de carga que origino la gestion. |
| id_cartera | BIGINT | FK | Cartera o campana asociada. |
| id_usuario | BIGINT | FK | Usuario interno relacionado con la gestion. |
| fecha_gestion | TIMESTAMP | NOT NULL | Fecha y hora de la gestion. |
| dni | VARCHAR(15) | NOT NULL | Documento del cliente. |
| telefono | VARCHAR(20) | NULL | Telefono gestionado. |
| status | VARCHAR(30) | NOT NULL | Resultado general del contacto. |
| tipificacion | VARCHAR(120) | NOT NULL | Detalle operativo de la gestion. |
| observacion | TEXT | NULL | Comentario operativo. |
| fecha_pago | DATE | NULL | Fecha de pago o compromiso. |
| monto_pago | NUMERIC(12,2) | NULL | Monto de pago o compromiso. |
| nombre | VARCHAR(150) | NULL | Nombre asociado al registro. |
| clave_unica | VARCHAR(250) | UNIQUE, NOT NULL | Clave compuesta para evitar duplicados. |
| creado_en | TIMESTAMP | NOT NULL | Fecha de creacion del registro. |

## Reglas de limpieza

| Campo | Regla |
|---|---|
| dni | Conservar solo numeros. |
| telefono | Conservar solo numeros. |
| status | Limpiar espacios, convertir a mayusculas y homologar. |
| tipificacion | Limpiar espacios, convertir a mayusculas y homologar. |
| fecha_gestion | Convertir a fecha/hora valida. |
| fecha_pago | Permitir nulo o fecha valida. |
| monto_pago | Permitir nulo o decimal. |
| observacion | Quitar espacios innecesarios. |
| nombre | Quitar espacios innecesarios. |

