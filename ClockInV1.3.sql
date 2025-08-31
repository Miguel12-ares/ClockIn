-- Creación de la Base de Datos y Tablas para ClockIn
-- Tabla para tipos de usuario y permisos de los mismos
CREATE TABLE user_types (
id INT AUTO_INCREMENT PRIMARY KEY,
type_name VARCHAR(50) NOT NULL UNIQUE,
description TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Tabla para zonas (sedes)
CREATE TABLE zonas (
id INT AUTO_INCREMENT PRIMARY KEY,
sede_nombre VARCHAR(100) NOT NULL,
departamento VARCHAR(50) NOT NULL,
ciudad VARCHAR(50) NOT NULL
);
-- Tabla para estados de usuario o sistema extendidos
CREATE TABLE estados (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) NOT NULL UNIQUE,
description TEXT NULL
);
-- Tabla con usuarios (modificada para agregar passwordHash)
CREATE TABLE users (
id INT AUTO_INCREMENT PRIMARY KEY,
idDocumento INT UNIQUE NOT NULL,
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) NOT NULL,
passwordHash VARCHAR(255) NOT NULL,
user_type_id INT NOT NULL,
zona_id INT NOT NULL,
fingerprint_data LONGBLOB NULL,
is_active BOOLEAN NOT NULL DEFAULT TRUE,
estado_id INT NOT NULL DEFAULT 1, -- FK a estados
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
CONSTRAINT fk_user_type FOREIGN KEY (user_type_id) REFERENCES user_types(id),
CONSTRAINT fk_zona FOREIGN KEY (zona_id) REFERENCES zonas(id),
CONSTRAINT fk_estado FOREIGN KEY (estado_id) REFERENCES estados(id)
);
-- Tabla para relacionar admins con zonas que administran (usuarios con rol admin)
CREATE TABLE admin_zona (
admin_id INT NOT NULL,
zona_id INT NOT NULL,
PRIMARY KEY (admin_id, zona_id),
CONSTRAINT fk_admin FOREIGN KEY (admin_id) REFERENCES users(id),
CONSTRAINT fk_zona_admin FOREIGN KEY (zona_id) REFERENCES zonas(id)
);
-- Tabla para logs de acceso y acciones
CREATE TABLE access_logs (
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT NOT NULL,
action_type VARCHAR(100),
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
fingerprint_confidence DECIMAL(5,4) NULL,
status VARCHAR(50) NULL,
notes TEXT NULL,
created_by INT NULL,
CONSTRAINT fk_access_user FOREIGN KEY (user_id) REFERENCES users(id),
CONSTRAINT fk_created_by_user FOREIGN KEY (created_by) REFERENCES users(id)
);
-- Tabla para sesiones activas
CREATE TABLE active_sessions (
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT NOT NULL,
entry_time DATETIME NOT NULL,
status VARCHAR(50) NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT fk_active_user FOREIGN KEY (user_id) REFERENCES users(id)
);
-- Tabla para anomalías detectadas
CREATE TABLE anomalies (
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT NOT NULL,
anomaly_type VARCHAR(100) NOT NULL,
description TEXT NULL,
detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
resolved BOOLEAN DEFAULT FALSE,
resolved_at DATETIME NULL,
resolved_by INT NULL,
resolution_notes TEXT NULL,
CONSTRAINT fk_anomaly_user FOREIGN KEY (user_id) REFERENCES users(id),
CONSTRAINT fk_resolved_by_user FOREIGN KEY (resolved_by) REFERENCES users(id)
);
-- Tabla para auditoría sistema
CREATE TABLE system_audit (
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT NULL,
table_affected VARCHAR(100) NULL,
action_type VARCHAR(100) NULL,
old_values TEXT NULL,
new_values TEXT NULL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
ip_address VARCHAR(45) NULL,
CONSTRAINT fk_audit_user FOREIGN KEY (user_id) REFERENCES users(id)
);
-- Insercion de estados comunes para el sistema.
INSERT INTO estados (name, description) VALUES
('activo', 'Usuario activo'),
('inactivo', 'Usuario inactivo o suspendido'),
('pendiente', 'Estado pendiente de autorización o validación'),
('eliminado', 'Usuario o dato eliminado o inhabilitado');