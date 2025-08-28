"""
Script de migración para agregar el campo password_hash a la tabla users
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from app.models.user import User
from werkzeug.security import generate_password_hash
from sqlalchemy import text

def add_password_field():
    """Agregar campo password_hash a la tabla users"""
    with app.app_context():
        try:
            # Verificar si la columna ya existe
            result = db.session.execute(text("""
                SELECT COUNT(*) as count 
                FROM information_schema.columns 
                WHERE table_name = 'users' 
                AND column_name = 'password_hash'
            """))
            
            column_exists = result.fetchone()[0] > 0
            
            if not column_exists:
                # Agregar la columna password_hash
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN password_hash VARCHAR(255) NULL
                """))
                db.session.commit()
                print("✅ Campo password_hash agregado exitosamente")
            else:
                print("ℹ️ Campo password_hash ya existe")
            
            # Establecer contraseñas por defecto para usuarios existentes
            users = User.query.all()
            updated_count = 0
            
            for user in users:
                if user.password_hash is None:
                    # Contraseña por defecto: 123456
                    user.password_hash = generate_password_hash('123456')
                    updated_count += 1
            
            if updated_count > 0:
                db.session.commit()
                print(f"✅ Contraseñas por defecto establecidas para {updated_count} usuarios")
                print("   Contraseña por defecto: 123456")
            else:
                print("ℹ️ Todos los usuarios ya tienen contraseñas establecidas")
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    add_password_field()
