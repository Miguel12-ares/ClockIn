#!/usr/bin/env python3
"""
Script para ejecutar la migración de la base de datos
"""
import os
import sys

def run_migration():
    """Ejecutar migración de la base de datos"""
    print("🔄 Ejecutando migración de base de datos...")
    
    try:
        # Importar y ejecutar la migración
        from migrations.add_password_field import add_password_field
        add_password_field()
        print("✅ Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_migration()
