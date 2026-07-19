-- ============================================================
-- BASE ORIGEN ESCALL: escarperu_software
-- Ejecutar en phpMyAdmin con la base escarperu_software activa.
-- Este procedimiento solo realiza lectura sobre gestiones.
-- ============================================================

-- Revisar primero la estructura real. La aplicación repite esta validación.
SHOW COLUMNS FROM gestiones;

DROP PROCEDURE IF EXISTS sp_descargar_gestiones_rango;

DELIMITER $$

CREATE PROCEDURE sp_descargar_gestiones_rango(
    IN p_fecha_desde DATETIME,
    IN p_fecha_hasta DATETIME
)
BEGIN
    SELECT
        id,
        fecha_gestion,
        dni,
        telefono,
        status,
        tipificacion,
        observacion,
        fecha_pago,
        monto_pago,
        nombre,
        created_at,
        updated_at
    FROM gestiones
    WHERE fecha_gestion >= p_fecha_desde
      AND fecha_gestion < p_fecha_hasta
    ORDER BY fecha_gestion ASC, id ASC;
END $$

DELIMITER ;

-- Prueba de solo lectura. El limite final es exclusivo.
CALL sp_descargar_gestiones_rango(
    '2026-07-01 00:00:00',
    '2026-07-19 00:00:00'
);

-- Permisos minimos del usuario remoto de la aplicacion:
-- SELECT, EXECUTE y SHOW VIEW.
-- El usuario que crea la rutina requiere adicionalmente:
-- CREATE ROUTINE y ALTER ROUTINE.
