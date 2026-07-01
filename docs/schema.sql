CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE tipificaciones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE ejecuciones (
    id SERIAL PRIMARY KEY,
    fecha_inicio TIMESTAMP NOT NULL DEFAULT NOW(),
    fecha_fin TIMESTAMP,
    total_leidos INTEGER NOT NULL DEFAULT 0,
    total_limpios INTEGER NOT NULL DEFAULT 0,
    duplicados_eliminados INTEGER NOT NULL DEFAULT 0,
    archivo_generado TEXT
);

CREATE TABLE gestiones (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES empresas(id),
    tipificacion_id INTEGER REFERENCES tipificaciones(id),
    ejecucion_id INTEGER REFERENCES ejecuciones(id),
    fecha_gestion TIMESTAMP NOT NULL,
    dni VARCHAR(20) NOT NULL,
    telefono VARCHAR(30),
    status VARCHAR(50) NOT NULL,
    tipificacion VARCHAR(100) NOT NULL,
    observacion TEXT,
    fecha_pago TIMESTAMP,
    monto_pago NUMERIC(12, 2),
    nombre VARCHAR(150),
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE reportes_generados (
    id SERIAL PRIMARY KEY,
    ejecucion_id INTEGER REFERENCES ejecuciones(id),
    ruta_archivo TEXT NOT NULL,
    enviado BOOLEAN NOT NULL DEFAULT FALSE,
    creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

