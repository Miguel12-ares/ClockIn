#!/usr/bin/env python3
"""
Script para inicializar la base de datos del sistema ClockIn
con datos básicos como tipos de usuario, estados y zonas.
"""

import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.utils.init_data import init_all_data


def main():
    """
    Función principal para inicializar la base de datos
    """
    print("=== Inicializador de Base de Datos ClockIn ===")
    print("Este script creará las tablas y datos básicos necesarios")
    
    with app.app_context():
        try:
            # Crear todas las tablas
            print("\n1. Creando tablas de la base de datos...")
            db.create_all()
            print("✓ Tablas creadas correctamente")
            
            # Inicializar datos básicos
            print("\n2. Inicializando datos básicos...")
            init_all_data()
            print("✓ Datos básicos inicializados")
            
            print("\n=== Inicialización completada exitosamente ===")
            print("\nAhora puedes:")
            print("1. Crear usuarios usando el endpoint POST /users")
            print("2. Autenticarte usando POST /auth/login")
            print("3. Iniciar el servidor con: python run.py")
            
        except Exception as e:
            print(f"\n❌ Error durante la inicialización: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()
