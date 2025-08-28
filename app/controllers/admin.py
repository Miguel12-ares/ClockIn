from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.middleware.auth_middleware import admin_required
from app.models.user import User
from app.models.user_type import UserType
from app.models.zona import Zona
from app.models.estado import Estado
from app.models.admin_zona import AdminZona
from app.models.system_audit import SystemAudit
from sqlalchemy.exc import IntegrityError, OperationalError
import json
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def log_audit(user_id, table_affected, action_type, old_values=None, new_values=None, ip_address=None):
    """Función para registrar auditoría en system_audit"""
    try:
        audit_entry = SystemAudit(
            user_id=user_id,
            table_affected=table_affected,
            action_type=action_type,
            old_values=json.dumps(old_values) if old_values else None,
            new_values=json.dumps(new_values) if new_values else None,
            ip_address=ip_address or request.remote_addr
        )
        db.session.add(audit_entry)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error al registrar auditoría: {e}")

@admin_bp.route('/users')
@admin_required
def users_index():
    """Lista de usuarios con paginación y filtros"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        search = request.args.get('search', '')
        
        query = User.query.options(db.joinedload(User.zona), db.joinedload(User.user_type), db.joinedload(User.estado))
        
        if search:
            query = query.filter(
                db.or_(
                    User.first_name.contains(search),
                    User.last_name.contains(search),
                    User.idDocumento.contains(search)
                )
            )
        
        users = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('admin/users.html', users=users, search=search)
    except OperationalError as e:
        flash('Error de base de datos al cargar usuarios', 'error')
        return render_template('admin/users.html', users=None, search=search, error_message="Error de base de datos")
    except Exception as e:
        flash(f'Error al cargar usuarios: {str(e)}', 'error')
        return render_template('admin/users.html', users=None, search=search, error_message=str(e))

@admin_bp.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Crear nuevo usuario"""
    if request.method == 'GET':
        try:
            user_types = UserType.query.all()
            zonas = Zona.query.all()
            estados = Estado.query.all()
            return render_template('admin/user_form.html', 
                                user=None, 
                                user_types=user_types, 
                                zonas=zonas, 
                                estados=estados,
                                action='create')
        except Exception as e:
            flash(f'Error al cargar formulario: {str(e)}', 'error')
            return redirect('/')
    
    elif request.method == 'POST':
        try:
            # Validar datos requeridos
            required_fields = ['idDocumento', 'first_name', 'last_name', 'user_type_id', 'zona_id']
            for field in required_fields:
                if not request.form.get(field):
                    flash(f'El campo {field} es requerido', 'error')
                    return redirect('/admin/users/create')
            
            # Validar que idDocumento sea único
            existing_user = User.query.filter_by(idDocumento=request.form['idDocumento']).first()
            if existing_user:
                flash('El número de documento ya existe', 'error')
                return redirect('/admin/users/create')
            
            # Crear nuevo usuario
            new_user = User(
                idDocumento=request.form['idDocumento'],
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                user_type_id=request.form['user_type_id'],
                zona_id=request.form['zona_id'],
                estado_id=request.form.get('estado_id', 1),
                is_active=request.form.get('is_active', True, type=bool)
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            # Registrar auditoría
            log_audit(
                user_id=None,  # En desarrollo, no hay usuario autenticado
                table_affected='users',
                action_type='CREATE',
                new_values={
                    'idDocumento': new_user.idDocumento,
                    'first_name': new_user.first_name,
                    'last_name': new_user.last_name,
                    'user_type_id': new_user.user_type_id,
                    'zona_id': new_user.zona_id,
                    'estado_id': new_user.estado_id,
                    'is_active': new_user.is_active
                }
            )
            
            flash('Usuario creado exitosamente', 'success')
            return redirect('/admin/users')
            
        except IntegrityError as e:
            db.session.rollback()
            flash('Error de integridad en la base de datos', 'error')
            return redirect('/admin/users/create')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear usuario: {str(e)}', 'error')
            return redirect('/admin/users/create')

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Editar usuario existente"""
    try:
        user = User.query.get_or_404(user_id)
        
        if request.method == 'GET':
            user_types = UserType.query.all()
            zonas = Zona.query.all()
            estados = Estado.query.all()
            return render_template('admin/user_form.html', 
                                user=user, 
                                user_types=user_types, 
                                zonas=zonas, 
                                estados=estados,
                                action='edit')
        
        elif request.method == 'POST':
            # Guardar valores anteriores para auditoría
            old_values = {
                'idDocumento': user.idDocumento,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type_id': user.user_type_id,
                'zona_id': user.zona_id,
                'estado_id': user.estado_id,
                'is_active': user.is_active
            }
            
            # Validar datos requeridos
            required_fields = ['idDocumento', 'first_name', 'last_name', 'user_type_id', 'zona_id']
            for field in required_fields:
                if not request.form.get(field):
                    flash(f'El campo {field} es requerido', 'error')
                    return redirect(f'/admin/users/{user_id}/edit')
            
            # Validar que idDocumento sea único (excluyendo el usuario actual)
            existing_user = User.query.filter(
                User.idDocumento == request.form['idDocumento'],
                User.id != user_id
            ).first()
            if existing_user:
                flash('El número de documento ya existe', 'error')
                return redirect(f'/admin/users/{user_id}/edit')
            
            # Actualizar usuario
            user.idDocumento = request.form['idDocumento']
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.user_type_id = request.form['user_type_id']
            user.zona_id = request.form['zona_id']
            user.estado_id = request.form.get('estado_id', 1)
            user.is_active = request.form.get('is_active', True, type=bool)
            
            db.session.commit()
            
            # Registrar auditoría
            new_values = {
                'idDocumento': user.idDocumento,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type_id': user.user_type_id,
                'zona_id': user.zona_id,
                'estado_id': user.estado_id,
                'is_active': user.is_active
            }
            
            log_audit(
                user_id=None,
                table_affected='users',
                action_type='UPDATE',
                old_values=old_values,
                new_values=new_values
            )
            
            flash('Usuario actualizado exitosamente', 'success')
            return redirect('/admin/users')
            
    except IntegrityError as e:
        db.session.rollback()
        flash('Error de integridad en la base de datos', 'error')
        return redirect('/admin/users')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al editar usuario: {str(e)}', 'error')
        return redirect('/admin/users')

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Eliminar usuario"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Guardar datos para auditoría
        old_values = {
            'idDocumento': user.idDocumento,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type_id': user.user_type_id,
            'zona_id': user.zona_id,
            'estado_id': user.estado_id,
            'is_active': user.is_active
        }
        
        db.session.delete(user)
        db.session.commit()
        
        # Registrar auditoría
        log_audit(
            user_id=None,
            table_affected='users',
            action_type='DELETE',
            old_values=old_values
        )
        
        flash('Usuario eliminado exitosamente', 'success')
        return redirect('/admin/users')
        
    except IntegrityError as e:
        db.session.rollback()
        flash('No se puede eliminar el usuario debido a restricciones de integridad', 'error')
        return redirect('/admin/users')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar usuario: {str(e)}', 'error')
        return redirect('/admin/users')

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    """Activar/desactivar usuario"""
    try:
        user = User.query.get_or_404(user_id)
        old_status = user.is_active
        user.is_active = not user.is_active
        
        db.session.commit()
        
        # Registrar auditoría
        log_audit(
            user_id=None,
            table_affected='users',
            action_type='TOGGLE_STATUS',
            old_values={'is_active': old_status},
            new_values={'is_active': user.is_active}
        )
        
        status_text = 'activado' if user.is_active else 'desactivado'
        flash(f'Usuario {status_text} exitosamente', 'success')
        return redirect('/admin/users')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado del usuario: {str(e)}', 'error')
        return redirect('/admin/users')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Dashboard administrativo"""
    try:
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        inactive_users = User.query.filter_by(is_active=False).count()
        
        # Estadísticas por tipo de usuario (simplificado para evitar errores de JOIN)
        user_types_stats = []
        try:
            user_types_stats = db.session.query(
                UserType.type_name,
                db.func.count(User.id).label('count')
            ).join(User, UserType.id == User.user_type_id).group_by(UserType.id, UserType.type_name).all()
        except Exception as e:
            print(f"Error en estadísticas de tipos de usuario: {e}")
            # Fallback: mostrar tipos sin estadísticas
            user_types = UserType.query.all()
            user_types_stats = [(ut.type_name, 0) for ut in user_types]
        
        # Estadísticas por zona usando ORM
        zonas_stats = []
        try:
            zonas_stats = db.session.query(
                Zona.nombre,
                db.func.count(User.id).label('count')
            ).join(User, Zona.id == User.zona_id).group_by(Zona.id, Zona.nombre).all()
        except Exception as e:
            print(f"Error en estadísticas de zonas: {e}")
            # Fallback: mostrar zonas sin estadísticas
            zonas = Zona.query.all()
            zonas_stats = [(z.nombre, 0) for z in zonas]
        
        return render_template('admin/dashboard.html',
                             total_users=total_users,
                             active_users=active_users,
                             inactive_users=inactive_users,
                             user_types_stats=user_types_stats,
                             zonas_stats=zonas_stats)
    except OperationalError as e:
        # Error de base de datos
        print(f"Error de base de datos en dashboard: {e}")
        return render_template('admin/dashboard.html',
                             total_users=0,
                             active_users=0,
                             inactive_users=0,
                             user_types_stats=[],
                             zonas_stats=[],
                             error_message="Error de base de datos al cargar estadísticas")
    except Exception as e:
        # Error general
        print(f"Error en dashboard: {e}")
        return render_template('admin/dashboard.html',
                             total_users=0,
                             active_users=0,
                             inactive_users=0,
                             user_types_stats=[],
                             zonas_stats=[],
                             error_message=f"Error al cargar estadísticas: {str(e)}")

# -------------------- Zonas (Web) --------------------

@admin_bp.route('/zonas', methods=['GET'])
@admin_required
def zonas_index():
    """Lista y gestiona zonas (vista HTML)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        query = Zona.query.options(
            db.selectinload(Zona.users),
            db.selectinload(Zona.admins)
        ).order_by(Zona.nombre)

        zonas_page = query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template('admin/zonas.html', zonas=zonas_page)
    except Exception as e:
        flash(f'Error al cargar zonas: {str(e)}', 'error')
        return render_template('admin/zonas.html', zonas=None, error_message=str(e))


@admin_bp.route('/zonas', methods=['POST'])
@admin_required
def zonas_create():
    """Crear zona (form HTML). Devuelve redirect con flash."""
    try:
        nombre = request.form.get('nombre', '').strip()
        departamento = request.form.get('departamento', '').strip()
        ciudad = request.form.get('ciudad', '').strip()
        if not nombre:
            flash('El nombre de la zona es requerido', 'error')
            return redirect(url_for('admin.zonas_index'))

        nueva = Zona(nombre=nombre, departamento=departamento or None, ciudad=ciudad or None)
        db.session.add(nueva)
        db.session.commit()

        log_audit(None, 'zonas', 'CREATE', old_values=None, new_values={'nombre': nombre, 'departamento': departamento, 'ciudad': ciudad})
        flash('Zona creada exitosamente', 'success')
        return redirect(url_for('admin.zonas_index'))
    except IntegrityError:
        db.session.rollback()
        flash('No se pudo crear la zona (duplicado u otro error de integridad)', 'error')
        return redirect(url_for('admin.zonas_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear zona: {str(e)}', 'error')
        return redirect(url_for('admin.zonas_index'))


@admin_bp.route('/zonas/<int:zona_id>', methods=['PUT', 'PATCH'])
@admin_required
def zonas_update(zona_id):
    """Editar zona (AJAX JSON). Devuelve JSON."""
    try:
        zona = Zona.query.get_or_404(zona_id)
        payload = request.get_json(silent=True) or {}
        old_values = {'nombre': zona.nombre, 'departamento': zona.departamento, 'ciudad': zona.ciudad}

        zona.nombre = (payload.get('nombre') or zona.nombre).strip()
        zona.departamento = (payload.get('departamento') or zona.departamento)
        zona.ciudad = (payload.get('ciudad') or zona.ciudad)

        db.session.commit()

        log_audit(None, 'zonas', 'UPDATE', old_values=old_values, new_values={'nombre': zona.nombre, 'departamento': zona.departamento, 'ciudad': zona.ciudad})
        return jsonify({'success': True, 'message': 'Zona actualizada', 'data': {'id': zona.id}}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@admin_bp.route('/zonas/<int:zona_id>', methods=['DELETE'])
@admin_required
def zonas_delete(zona_id):
    """Eliminar zona (AJAX JSON). Devuelve JSON."""
    try:
        zona = Zona.query.get_or_404(zona_id)
        old_values = {'nombre': zona.nombre, 'departamento': zona.departamento, 'ciudad': zona.ciudad}
        db.session.delete(zona)
        db.session.commit()
        log_audit(None, 'zonas', 'DELETE', old_values=old_values, new_values=None)
        return jsonify({'success': True, 'message': 'Zona eliminada'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


# -------------------- Tipos de Usuario (Web) --------------------

@admin_bp.route('/user_types', methods=['GET'])
@admin_required
def user_types_index():
    """Lista y gestiona tipos de usuario (vista HTML)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        query = UserType.query.order_by(UserType.type_name)
        types_page = query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template('admin/user_types.html', user_types=types_page)
    except Exception as e:
        flash(f'Error al cargar tipos de usuario: {str(e)}', 'error')
        return render_template('admin/user_types.html', user_types=None, error_message=str(e))


@admin_bp.route('/user_types', methods=['POST'])
@admin_required
def user_types_create():
    """Crear tipo de usuario (form HTML)."""
    try:
        type_name = request.form.get('type_name', '').strip()
        description = request.form.get('description', '').strip()
        if not type_name:
            flash('El nombre del tipo es requerido', 'error')
            return redirect(url_for('admin.user_types_index'))

        nuevo = UserType(type_name=type_name, description=description or None)
        db.session.add(nuevo)
        db.session.commit()

        log_audit(None, 'user_types', 'CREATE', old_values=None, new_values={'type_name': type_name, 'description': description})
        flash('Tipo de usuario creado exitosamente', 'success')
        return redirect(url_for('admin.user_types_index'))
    except IntegrityError:
        db.session.rollback()
        flash('No se pudo crear el tipo (duplicado u otro error de integridad)', 'error')
        return redirect(url_for('admin.user_types_index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear tipo: {str(e)}', 'error')
        return redirect(url_for('admin.user_types_index'))


@admin_bp.route('/user_types/<int:type_id>', methods=['PUT', 'PATCH'])
@admin_required
def user_types_update(type_id):
    """Editar tipo (AJAX JSON)."""
    try:
        ut = UserType.query.get_or_404(type_id)
        payload = request.get_json(silent=True) or {}
        old_values = {'type_name': ut.type_name, 'description': ut.description}

        ut.type_name = (payload.get('type_name') or ut.type_name).strip()
        ut.description = payload.get('description') or ut.description
        db.session.commit()

        log_audit(None, 'user_types', 'UPDATE', old_values=old_values, new_values={'type_name': ut.type_name, 'description': ut.description})
        return jsonify({'success': True, 'message': 'Tipo actualizado', 'data': {'id': ut.id}}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@admin_bp.route('/user_types/<int:type_id>', methods=['DELETE'])
@admin_required
def user_types_delete(type_id):
    """Eliminar tipo (AJAX JSON)."""
    try:
        ut = UserType.query.get_or_404(type_id)
        old_values = {'type_name': ut.type_name, 'description': ut.description}
        db.session.delete(ut)
        db.session.commit()
        log_audit(None, 'user_types', 'DELETE', old_values=old_values, new_values=None)
        return jsonify({'success': True, 'message': 'Tipo eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400
