-- ============================================================
-- BASE DESTINO LOCAL: automatizacion_gestiones
-- Ejecutar con un usuario local autorizado para crear esquemas.
-- ============================================================

CREATE DATABASE IF NOT EXISTS automatizacion_gestiones
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE automatizacion_gestiones;

CREATE TABLE IF NOT EXISTS empresas (
    id_empresa BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre_empresa VARCHAR(180) NOT NULL,
    ruc VARCHAR(20) NULL,
    estado ENUM('ACTIVO', 'INACTIVO') NOT NULL DEFAULT 'ACTIVO',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_empresas_ruc (ruc),
    INDEX idx_empresas_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_empresa BIGINT NULL,
    nombre VARCHAR(180) NOT NULL,
    correo VARCHAR(180) NULL,
    rol VARCHAR(80) NULL,
    estado ENUM('ACTIVO', 'INACTIVO') NOT NULL DEFAULT 'ACTIVO',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_usuarios_correo (correo),
    INDEX idx_usuarios_empresa (id_empresa),
    CONSTRAINT fk_usuarios_empresa FOREIGN KEY (id_empresa)
        REFERENCES empresas(id_empresa) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS carteras (
    id_cartera BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_empresa BIGINT NOT NULL,
    nombre_cartera VARCHAR(180) NOT NULL,
    descripcion VARCHAR(255) NULL,
    estado ENUM('ACTIVO', 'INACTIVO') NOT NULL DEFAULT 'ACTIVO',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_carteras_empresa (id_empresa),
    INDEX idx_carteras_estado (estado),
    CONSTRAINT fk_carteras_empresa FOREIGN KEY (id_empresa)
        REFERENCES empresas(id_empresa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS control_descargas_gestiones (
    id_control BIGINT AUTO_INCREMENT PRIMARY KEY,
    fecha_desde DATETIME NOT NULL,
    fecha_hasta DATETIME NOT NULL,
    estado ENUM('PENDIENTE', 'EN_PROCESO', 'FINALIZADO', 'ERROR')
        NOT NULL DEFAULT 'PENDIENTE',
    tipo_descarga ENUM('MANUAL', 'AUTOMATICA') NOT NULL DEFAULT 'MANUAL',
    registros_origen INT NOT NULL DEFAULT 0,
    registros_insertados INT NOT NULL DEFAULT 0,
    registros_duplicados INT NOT NULL DEFAULT 0,
    registros_invalidos INT NOT NULL DEFAULT 0,
    mensaje_error TEXT NULL,
    descripcion VARCHAR(255) NULL,
    fecha_inicio_proceso DATETIME NULL,
    fecha_fin_proceso DATETIME NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_control_estado_fecha (estado, fecha_desde),
    CONSTRAINT chk_control_rango CHECK (fecha_hasta > fecha_desde)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS cargas_gestiones (
    id_carga BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_control_descarga BIGINT NULL,
    nombre_fuente VARCHAR(180) NOT NULL DEFAULT 'ESCALL_SP',
    estado ENUM('INICIADO', 'FINALIZADO', 'ERROR') NOT NULL DEFAULT 'INICIADO',
    registros_descargados INT NOT NULL DEFAULT 0,
    registros_insertados INT NOT NULL DEFAULT 0,
    registros_duplicados INT NOT NULL DEFAULT 0,
    registros_invalidos INT NOT NULL DEFAULT 0,
    mensaje_error TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_cargas_control (id_control_descarga),
    CONSTRAINT fk_cargas_control FOREIGN KEY (id_control_descarga)
        REFERENCES control_descargas_gestiones(id_control) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS gestiones_procesadas (
    id_procesado BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_gestion_origen BIGINT NOT NULL,
    fecha_gestion DATETIME NOT NULL,
    dni VARCHAR(20) NOT NULL,
    telefono VARCHAR(30) NULL,
    status_original VARCHAR(100) NULL,
    tipificacion_original VARCHAR(150) NULL,
    status_homologado VARCHAR(50) NOT NULL,
    tipificacion_homologada VARCHAR(150) NOT NULL,
    observacion TEXT NULL,
    fecha_pago DATE NULL,
    monto_pago DECIMAL(14, 2) NULL,
    nombre_asesor VARCHAR(150) NULL,
    clave_unica CHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
    id_control_descarga BIGINT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_gestiones_clave_unica (clave_unica),
    INDEX idx_gestiones_id_origen (id_gestion_origen),
    INDEX idx_gestiones_fecha (fecha_gestion),
    INDEX idx_gestiones_dni (dni),
    INDEX idx_gestiones_asesor (nombre_asesor),
    INDEX idx_gestiones_status (status_homologado),
    INDEX idx_gestiones_fecha_pago (fecha_pago),
    INDEX idx_gestiones_control (id_control_descarga),
    CONSTRAINT fk_gestiones_control FOREIGN KEY (id_control_descarga)
        REFERENCES control_descargas_gestiones(id_control) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS reportes (
    id_reporte BIGINT AUTO_INCREMENT PRIMARY KEY,
    tipo_reporte VARCHAR(100) NOT NULL,
    fecha_desde DATETIME NULL,
    fecha_hasta DATETIME NULL,
    ruta_archivo VARCHAR(500) NULL,
    estado ENUM('GENERADO', 'ERROR') NOT NULL DEFAULT 'GENERADO',
    mensaje_error TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_reportes_tipo_fecha (tipo_reporte, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS destinatarios_reportes (
    id_destinatario BIGINT AUTO_INCREMENT PRIMARY KEY,
    tipo_reporte VARCHAR(100) NOT NULL,
    nombre VARCHAR(180) NULL,
    correo VARCHAR(180) NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_destinatario_tipo_correo (tipo_reporte, correo),
    INDEX idx_destinatarios_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS envios_reportes (
    id_envio BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_reporte BIGINT NULL,
    id_destinatario BIGINT NULL,
    tipo_reporte VARCHAR(100) NOT NULL,
    destinatario VARCHAR(180) NOT NULL,
    asunto VARCHAR(255) NOT NULL,
    estado_envio ENUM('PENDIENTE', 'ENVIADO', 'ERROR')
        NOT NULL DEFAULT 'PENDIENTE',
    mensaje_error TEXT NULL,
    fecha_envio DATETIME NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_envios_tipo_estado (tipo_reporte, estado_envio),
    INDEX idx_envios_fecha (fecha_envio),
    CONSTRAINT fk_envios_reporte FOREIGN KEY (id_reporte)
        REFERENCES reportes(id_reporte) ON DELETE SET NULL,
    CONSTRAINT fk_envios_destinatario FOREIGN KEY (id_destinatario)
        REFERENCES destinatarios_reportes(id_destinatario) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS logs_proceso (
    id_log BIGINT AUTO_INCREMENT PRIMARY KEY,
    proceso VARCHAR(100) NOT NULL,
    nivel ENUM('INFO', 'ADVERTENCIA', 'ERROR') NOT NULL DEFAULT 'INFO',
    mensaje TEXT NOT NULL,
    id_control_descarga BIGINT NULL,
    detalle_error TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_logs_proceso_fecha (proceso, created_at),
    INDEX idx_logs_nivel (nivel),
    INDEX idx_logs_control (id_control_descarga),
    CONSTRAINT fk_logs_control FOREIGN KEY (id_control_descarga)
        REFERENCES control_descargas_gestiones(id_control) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
