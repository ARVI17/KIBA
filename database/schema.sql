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
