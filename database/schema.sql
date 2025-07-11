-- database/schema.sql

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol_id INTEGER,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

-- Datos iniciales
INSERT INTO roles (nombre) VALUES ('Administrador'), ('Operador');

-- Usuario de ejemplo: admin@citamatic.com / contraseña: admin123 (encriptar luego)
INSERT INTO usuarios (correo, contrasena, rol_id)
VALUES ('admin@citamatic.com', 'admin123', 1);

CREATE TABLE especialidades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE sms (
    id SERIAL PRIMARY KEY,
    celular VARCHAR(20) NOT NULL,
    mensaje TEXT NOT NULL,
    especialidad_id INTEGER,
    fecha_envio TIMESTAMP,
    estado VARCHAR(50),
    token_confirmacion VARCHAR(50) UNIQUE,
    confirmado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (especialidad_id) REFERENCES especialidades(id)
);

CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    celular VARCHAR(20) NOT NULL UNIQUE,
    especialidad_id INTEGER NOT NULL,
    programada TIMESTAMP,
    FOREIGN KEY (especialidad_id) REFERENCES especialidades(id)
);

CREATE TABLE citas (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL,
    especialidad_id INTEGER NOT NULL,
    fecha_hora TIMESTAMP NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (especialidad_id) REFERENCES especialidades(id)
);

CREATE TABLE confirmaciones (
    id SERIAL PRIMARY KEY,
    cita_id INTEGER NOT NULL,
    sms_id INTEGER NOT NULL,
    confirmada_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cita_id) REFERENCES citas(id),
    FOREIGN KEY (sms_id) REFERENCES sms(id)
);

CREATE TABLE sms_pendientes (
    id SERIAL PRIMARY KEY,
    celular VARCHAR(20) NOT NULL,
    mensaje TEXT NOT NULL,
    especialidad VARCHAR(100),
    fecha_programada TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'pendiente'
);

-- Índices
CREATE INDEX idx_pacientes_especialidad ON pacientes (especialidad_id);
CREATE INDEX idx_citas_paciente ON citas (paciente_id);
CREATE INDEX idx_citas_especialidad ON citas (especialidad_id);
CREATE INDEX idx_confirmaciones_cita ON confirmaciones (cita_id);
CREATE INDEX idx_confirmaciones_sms ON confirmaciones (sms_id);
