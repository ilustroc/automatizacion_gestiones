-- ============================================================
-- VISTAS DE LA BASE DESTINO LOCAL
-- Ejecutar despues de 02_target_local_schema.sql.
-- ============================================================

USE automatizacion_gestiones;

DROP VIEW IF EXISTS vw_ranking_gerencia_asesores_dia;
DROP VIEW IF EXISTS vw_reporte_gerencia_asesores_dia;
DROP VIEW IF EXISTS vw_reporte_impulse_gestiones;
DROP VIEW IF EXISTS vw_alerta_promesas_pago;
DROP VIEW IF EXISTS vw_control_descargas_pendientes;

CREATE VIEW vw_control_descargas_pendientes AS
SELECT
    id_control,
    fecha_desde,
    fecha_hasta,
    estado,
    tipo_descarga,
    registros_origen,
    registros_insertados,
    registros_duplicados,
    registros_invalidos,
    descripcion,
    created_at,
    updated_at
FROM control_descargas_gestiones
WHERE estado = 'PENDIENTE';

CREATE VIEW vw_alerta_promesas_pago AS
SELECT
    fecha_gestion,
    dni,
    telefono,
    nombre_asesor,
    fecha_pago,
    monto_pago,
    tipificacion_homologada,
    observacion,
    DATEDIFF(fecha_pago, CURDATE()) AS dias_diferencia,
    CASE
        WHEN fecha_pago < CURDATE() THEN 'VENCIDA'
        WHEN fecha_pago = CURDATE() THEN 'VENCE HOY'
        WHEN fecha_pago = DATE_ADD(CURDATE(), INTERVAL 1 DAY) THEN 'VENCE MAÑANA'
        ELSE 'PRÓXIMA'
    END AS nivel_alerta
FROM gestiones_procesadas
WHERE fecha_pago IS NOT NULL
  AND tipificacion_homologada = 'PROMESA DE PAGO';

CREATE VIEW vw_reporte_impulse_gestiones AS
SELECT
    fecha_gestion,
    dni,
    telefono,
    status_homologado,
    tipificacion_homologada,
    observacion,
    fecha_pago,
    monto_pago,
    nombre_asesor
FROM gestiones_procesadas;

CREATE VIEW vw_reporte_gerencia_asesores_dia AS
SELECT
    DATE(fecha_gestion) AS fecha,
    COALESCE(nombre_asesor, 'SIN ASESOR') AS nombre_asesor,
    COUNT(*) AS total_gestiones,
    SUM(CASE WHEN status_homologado = 'DIRECTO' THEN 1 ELSE 0 END)
        AS contactos_directos,
    SUM(CASE WHEN status_homologado = 'INDIRECTO' THEN 1 ELSE 0 END)
        AS contactos_indirectos,
    SUM(CASE WHEN status_homologado = 'NO CONTACTO' THEN 1 ELSE 0 END)
        AS no_contactos,
    SUM(CASE WHEN tipificacion_homologada = 'PROMESA DE PAGO' THEN 1 ELSE 0 END)
        AS total_promesas,
    SUM(
        CASE WHEN tipificacion_homologada = 'PROMESA DE PAGO'
             THEN COALESCE(monto_pago, 0) ELSE 0 END
    ) AS monto_prometido,
    COUNT(DISTINCT dni) AS clientes_unicos
FROM gestiones_procesadas
GROUP BY DATE(fecha_gestion), COALESCE(nombre_asesor, 'SIN ASESOR');

-- Verificar primero con SELECT VERSION(). MySQL 8+ y MariaDB 10.2+
-- admiten DENSE_RANK. Si la version es anterior, omitir esta vista:
-- ReporteGerenciaService calcula el mismo ranking desde Python.
CREATE VIEW vw_ranking_gerencia_asesores_dia AS
SELECT
    resumen.*,
    DENSE_RANK() OVER (
        PARTITION BY fecha
        ORDER BY total_gestiones DESC
    ) AS ranking_diario
FROM vw_reporte_gerencia_asesores_dia AS resumen;
