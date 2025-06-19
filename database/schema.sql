-- database/schema.sql

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100) UNIQUE,
    contrasena VARCHAR(255),
    rol_id INTEGER,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

-- Datos iniciales
INSERT INTO roles (nombre) VALUES ('Administrador'), ('Operador');

-- Usuario de ejemplo: admin@kiba.com / contraseña: admin123 (encriptar luego)
INSERT INTO usuarios (nombre, correo, contrasena, rol_id)
VALUES ('Admin Kiba', 'admin@kiba.com', 'admin123', 1);

CREATE TABLE sms (
    id SERIAL PRIMARY KEY,
    numero VARCHAR(20),
    mensaje TEXT,
    estado VARCHAR(50),
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE especialidades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
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


-- Índices
CREATE INDEX idx_pacientes_especialidad ON pacientes (especialidad_id);
CREATE INDEX idx_citas_paciente ON citas (paciente_id);
CREATE INDEX idx_citas_especialidad ON citas (especialidad_id);
CREATE INDEX idx_confirmaciones_cita ON confirmaciones (cita_id);
CREATE INDEX idx_confirmaciones_sms ON confirmaciones (sms_id);
