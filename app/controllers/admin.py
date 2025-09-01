from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.models.user import User
from app.models.user_type import UserType
from app.models.zona import Zona
from app.models.estado import Estado
from app.models.system_audit import SystemAudit
from app import db
from functools import wraps
from sqlalchemy import cast, String

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'admin':
            flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/usuarios')
@admin_required
def usuarios():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = User.query
    if search:
        query = query.filter(
            (User.first_name.contains(search)) |
            (User.last_name.contains(search)) |
            (cast(User.idDocumento, String).contains(search))
        )
    
    users = query.paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/usuarios.html', users=users, search=search)

@admin_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_usuario():
    if request.method == 'POST':
        # Validar datos
        id_documento = request.form.get('idDocumento')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        user_type_id = request.form.get('user_type_id')
        zona_id = request.form.get('zona_id')
        
        # Verificar que no exista el usuario
        existing_user = User.query.filter_by(idDocumento=id_documento).first()
        if existing_user:
            flash('Ya existe un usuario con este ID de documento', 'error')
            return redirect(request.url)
        
        # Crear usuario
        new_user = User(
            idDocumento=id_documento,
            first_name=first_name,
            last_name=last_name,
            user_type_id=user_type_id,
            zona_id=zona_id,
            estado_id=1  # Activo por defecto
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.flush()  # Para obtener el ID
        
        # Auditoría
        audit = SystemAudit(
            user_id=session['user_id'],
            table_affected='users',
            action_type='CREATE',
            new_values=f"Usuario creado: {first_name} {last_name} (ID: {id_documento})",
            ip_address=request.remote_addr
        )
        db.session.add(audit)
        db.session.commit()
        
        flash(f'Usuario {first_name} {last_name} creado exitosamente', 'success')
        return redirect(url_for('admin.usuarios'))
    
    # GET - mostrar formulario
    user_types = UserType.query.all()
    zonas = Zona.query.all()
    return render_template('admin/usuario_form.html', user_types=user_types, zonas=zonas)

@admin_bp.route('/usuarios/<int:user_id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_usuario(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Guardar valores anteriores para auditoría
        old_values = f"Nombre: {user.first_name} {user.last_name}, Tipo: {user.user_type.type_name}, Zona: {user.zona.sede_nombre}"
        
        # Actualizar datos
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.user_type_id = request.form.get('user_type_id')
        user.zona_id = request.form.get('zona_id')
        user.estado_id = request.form.get('estado_id')
        
        # Cambiar contraseña si se proporciona
        new_password = request.form.get('password')
        if new_password:
            user.set_password(new_password)
        
        new_values = f"Nombre: {user.first_name} {user.last_name}, Tipo: {user.user_type.type_name}, Zona: {user.zona.sede_nombre}"
        
        # Auditoría
        audit = SystemAudit(
            user_id=session['user_id'],
            table_affected='users',
            action_type='UPDATE',
            old_values=old_values,
            new_values=new_values,
            ip_address=request.remote_addr
        )
        db.session.add(audit)
        db.session.commit()
        
        flash(f'Usuario {user.first_name} {user.last_name} actualizado exitosamente', 'success')
        return redirect(url_for('admin.usuarios'))
    
    # GET - mostrar formulario
    user_types = UserType.query.all()
    zonas = Zona.query.all()
    estados = Estado.query.all()
    return render_template('admin/usuario_form.html', 
                         user=user, user_types=user_types, zonas=zonas, estados=estados)

@admin_bp.route('/usuarios/<int:user_id>/eliminar', methods=['POST'])
@admin_required
def eliminar_usuario(user_id):
    user = User.query.get_or_404(user_id)
    
    # No permitir eliminar el usuario actual
    if user.id == session['user_id']:
        flash('No puedes eliminar tu propio usuario', 'error')
        return redirect(url_for('admin.usuarios'))
    
    # Auditoría antes de eliminar
    audit = SystemAudit(
        user_id=session['user_id'],
        table_affected='users',
        action_type='DELETE',
        old_values=f"Usuario eliminado: {user.first_name} {user.last_name} (ID: {user.idDocumento})",
        ip_address=request.remote_addr
    )
    db.session.add(audit)
    
    # Eliminar usuario
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Usuario {user.first_name} {user.last_name} eliminado exitosamente', 'success')
    return redirect(url_for('admin.usuarios'))

@admin_bp.route('/auditoria')
@admin_required
def auditoria():
    page = request.args.get('page', 1, type=int)
    audits = SystemAudit.query.order_by(SystemAudit.timestamp.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/auditoria.html', audits=audits)
