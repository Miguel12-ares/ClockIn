#!/usr/bin/env python3
from sqlalchemy import text
from app import create_app, db

app = create_app()

with app.app_context():
    print("=== DEBUG BASE DE DATOS ===")
    try:
        # Listar tablas
        result = db.session.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        print(f"📋 Tablas encontradas: {tables}")

        if 'users' in tables:
            result = db.session.execute(text("SELECT COUNT(*) FROM users"))
            count = result.scalar() or 0
            print(f"👥 Usuarios en DB: {count}")
        else:
            print("❌ Tabla 'users' no existe")
    except Exception as e:
        print(f"❌ Error conectando a DB: {e}")
