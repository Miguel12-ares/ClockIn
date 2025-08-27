from app import app, db
from app.init_data import init_basic_data
import time
import sys

def init_database():
    """Inicializa la base de datos con reintentos"""
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            print(f"Intento {attempt + 1}/{max_retries}: Conectando a la base de datos...")
            
            with app.app_context():
                # Importar modelos para registrar metadatos antes de crear tablas
                from app import models  # noqa: F401
                # Crear tablas
                db.create_all()
                print("✅ Tablas creadas exitosamente")
                
                # Inicializar datos básicos
                init_basic_data()
                print("✅ Datos básicos inicializados")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en intento {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Esperando {retry_delay} segundos antes del siguiente intento...")
                time.sleep(retry_delay)
            else:
                print("❌ Falló la inicialización de la base de datos después de todos los intentos")
                return False

if __name__ == '__main__':
    print("Iniciando ClockIn - Sistema de Control de Acceso")
    print("=" * 50)
    
    # Inicializar base de datos
    if not init_database():
        print("No se pudo inicializar la base de datos. Saliendo...")
        sys.exit(1)
    
    print("Sistema iniciado correctamente")
    print("Servidor disponible en: http://localhost:5000")
    print("Panel administrativo: http://localhost:5000/admin/dashboard")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
