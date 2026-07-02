-- Base de datos: automatizacion_gestiones
-- Motor propuesto: PostgreSQL / Supabase
-- Schema: public

CREATE TABLE IF NOT EXISTS empresas (
    id_empresa BIGSERIAL PRIMARY KEY,
    nombre_empresa VARCHAR(120) NOT NULL,
    ruc VARCHAR(20),
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO',
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(150) UNIQUE,
    rol VARCHAR(30) NOT NULL CHECK (rol IN ('ADMINISTRADOR', 'SUPERVISOR', 'ANALISTA', 'ASESOR')),
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO',
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS carteras (
    id_cartera BIGSERIAL PRIMARY KEY,
    id_empresa BIGINT NOT NULL REFERENCES empresas(id_empresa),
    nombre_cartera VARCHAR(120) NOT NULL,
    descripcion TEXT,
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO',
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cargas_gestiones (
    id_carga BIGSERIAL PRIMARY KEY,
    fecha_inicio TIMESTAMP NOT NULL DEFAULT NOW(),
    fecha_fin TIMESTAMP,
    periodo_desde DATE NOT NULL,
    periodo_hasta DATE NOT NULL,
    origen VARCHAR(50) NOT NULL DEFAULT 'STORED_PROCEDURE',
    nombre_sp VARCHAR(150),
    registros_descargados INT NOT NULL DEFAULT 0,
    registros_insertados INT NOT NULL DEFAULT 0,
    registros_duplicados INT NOT NULL DEFAULT 0,
    estado VARCHAR(30) NOT NULL DEFAULT 'INICIADO',
    observacion TEXT
);

CREATE TABLE IF NOT EXISTS gestiones (
    id_gestion BIGSERIAL PRIMARY KEY,
    id_carga BIGINT NOT NULL REFERENCES cargas_gestiones(id_carga),
    id_cartera BIGINT REFERENCES carteras(id_cartera),
    id_usuario BIGINT REFERENCES usuarios(id_usuario),
    fecha_gestion TIMESTAMP NOT NULL,
    dni VARCHAR(15) NOT NULL,
    telefono VARCHAR(20),
    status VARCHAR(30) NOT NULL CHECK (status IN ('DIRECTO', 'INDIRECTO', 'NO CONTACTO', 'SIN GESTION')),
    tipificacion VARCHAR(120) NOT NULL,
    observacion TEXT,
    fecha_pago DATE,
    monto_pago NUMERIC(12, 2),
    nombre VARCHAR(150),
    clave_unica VARCHAR(250) NOT NULL UNIQUE,
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reportes (
    id_reporte BIGSERIAL PRIMARY KEY,
    tipo_reporte VARCHAR(50) NOT NULL CHECK (tipo_reporte IN ('OPERATIVO', 'PRODUCCION', 'PROMESAS', 'GERENCIAL')),
    periodo_desde DATE NOT NULL,
    periodo_hasta DATE NOT NULL,
    ruta_archivo TEXT,
    fecha_generacion TIMESTAMP NOT NULL DEFAULT NOW(),
    estado VARCHAR(30) NOT NULL DEFAULT 'GENERADO'
);

CREATE TABLE IF NOT EXISTS destinatarios_reportes (
    id_destinatario BIGSERIAL PRIMARY KEY,
    id_empresa BIGINT REFERENCES empresas(id_empresa),
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(150) NOT NULL,
    tipo_destinatario VARCHAR(30) NOT NULL CHECK (tipo_destinatario IN ('EMPRESA', 'SUPERVISOR', 'ADMINISTRADOR')),
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO'
);

CREATE TABLE IF NOT EXISTS envios_reportes (
    id_envio BIGSERIAL PRIMARY KEY,
    id_reporte BIGINT NOT NULL REFERENCES reportes(id_reporte),
    id_destinatario BIGINT NOT NULL REFERENCES destinatarios_reportes(id_destinatario),
    fecha_envio TIMESTAMP NOT NULL DEFAULT NOW(),
    estado_envio VARCHAR(30) NOT NULL DEFAULT 'PENDIENTE',
    mensaje_error TEXT
);

CREATE TABLE IF NOT EXISTS logs_proceso (
    id_log BIGSERIAL PRIMARY KEY,
    id_carga BIGINT REFERENCES cargas_gestiones(id_carga),
    nivel VARCHAR(20) NOT NULL CHECK (nivel IN ('INFO', 'ADVERTENCIA', 'ERROR')),
    mensaje TEXT NOT NULL,
    fecha_log TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_gestiones_dni ON gestiones(dni);
CREATE INDEX IF NOT EXISTS idx_gestiones_fecha ON gestiones(fecha_gestion);
CREATE INDEX IF NOT EXISTS idx_gestiones_status ON gestiones(status);
CREATE INDEX IF NOT EXISTS idx_gestiones_tipificacion ON gestiones(tipificacion);
CREATE INDEX IF NOT EXISTS idx_gestiones_clave_unica ON gestiones(clave_unica);

CREATE OR REPLACE VIEW vw_resumen_gestiones AS
SELECT
    DATE(fecha_gestion) AS fecha,
    status,
    tipificacion,
    COUNT(*) AS total_gestiones,
    COUNT(DISTINCT dni) AS clientes_unicos,
    SUM(COALESCE(monto_pago, 0)) AS monto_total
FROM gestiones
GROUP BY DATE(fecha_gestion), status, tipificacion;

-- Datos minimos de ejemplo para una demostracion academica.
INSERT INTO empresas (nombre_empresa, ruc)
VALUES ('ESCALL PERU', '00000000000')
ON CONFLICT DO NOTHING;

INSERT INTO usuarios (nombre, correo, rol)
VALUES ('Analista de cobranza', 'analista@example.com', 'ANALISTA')
ON CONFLICT (correo) DO NOTHING;

INSERT INTO carteras (id_empresa, nombre_cartera, descripcion)
SELECT id_empresa, 'Cartera de ejemplo', 'Cartera academica de prueba'
FROM empresas
WHERE nombre_empresa = 'ESCALL PERU'
AND NOT EXISTS (
    SELECT 1
    FROM carteras
    WHERE nombre_cartera = 'Cartera de ejemplo'
);

