-- database/schema.sql

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100) UNIQUE,
    contrasena VARCHAR(255),
    rol_id INT,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

-- Datos iniciales
INSERT INTO roles (nombre) VALUES ('Administrador'), ('Operador');

-- Usuario de ejemplo: admin@kiba.com / contraseña: admin123 (encriptar luego)
INSERT INTO usuarios (nombre, correo, contrasena, rol_id)
VALUES ('Admin Kiba', 'admin@kiba.com', 'admin123', 1);


CREATE TABLE sms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(20),
    mensaje TEXT,
    estado VARCHAR(50),
    fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE especialidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    celular VARCHAR(20) NOT NULL UNIQUE,
    especialidad_id INT NOT NULL,
    programada DATETIME,
    FOREIGN KEY (especialidad_id) REFERENCES especialidades(id),
    INDEX idx_pacientes_especialidad (especialidad_id)
);

CREATE TABLE citas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    especialidad_id INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (especialidad_id) REFERENCES especialidades(id),
    INDEX idx_citas_paciente (paciente_id),
    INDEX idx_citas_especialidad (especialidad_id)
);

CREATE TABLE confirmaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cita_id INT NOT NULL,
    sms_id INT NOT NULL,
    confirmada_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cita_id) REFERENCES citas(id),
    FOREIGN KEY (sms_id) REFERENCES sms(id),
    INDEX idx_confirmaciones_cita (cita_id),
    INDEX idx_confirmaciones_sms (sms_id)
);

CREATE TABLE sms_pendientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    celular VARCHAR(20) NOT NULL,
    mensaje TEXT NOT NULL,
    especialidad VARCHAR(100),
    fecha_programada DATETIME,
    estado VARCHAR(20) DEFAULT 'pendiente'
);
