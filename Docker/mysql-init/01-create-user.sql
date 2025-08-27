-- Crear y asegurar permisos para el usuario 'user' con acceso desde cualquier host
CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'user_password';
GRANT ALL PRIVILEGES ON `db_name`.* TO 'user'@'%';
FLUSH PRIVILEGES;


