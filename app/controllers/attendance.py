from flask import Blueprint, request, jsonify, render_template, session, flash, redirect, url_for
from datetime import datetime, timezone
from sqlalchemy import func, and_, or_
from app import db
from app.models.user import User
from app.models.access_log import AccessLog
from app.models.active_session import ActiveSession
from app.models.system_audit import SystemAudit
from app.controllers.admin import admin_required

attendance_bp = Blueprint('attendance', __name__)

# Helpers

def _get_client_ip():
    # X-Forwarded-For support (behind reverse proxy)
    xff = request.headers.get('X-Forwarded-For')
    if xff:
        return xff.split(',')[0].strip()
    return request.remote_addr


def _find_user_by_document(doc_id: str | int) -> User | None:
    try:
        return User.query.filter_by(idDocumento=int(doc_id)).first()
    except Exception:
        return None


def _now_utc():
    return datetime.now(timezone.utc)


# API endpoints
@attendance_bp.route('/attendance/checkin', methods=['POST'])
def checkin():
    data = request.get_json(silent=True) or request.form
    doc_id = data.get('idDocumento')
    if not doc_id:
        return jsonify(success=False, error='idDocumento requerido'), 400

    user = _find_user_by_document(doc_id)
    if not user:
        return jsonify(success=False, error='Usuario no encontrado'), 404
    if not user.is_active or user.estado_id is None:
        return jsonify(success=False, error='Usuario inactivo'), 403

    # Verificar si hay sesión activa
    active = ActiveSession.query.filter_by(user_id=user.id).filter(ActiveSession.exit_time.is_(None)).first()
    if active:
        return jsonify(success=False, error='Ya hay una entrada activa (sin salida)'), 409

    now = _now_utc()

    # Crear AccessLog ENTRY
    entry_log = AccessLog(
        user_id=user.id,
        action_type='ENTRY',
        timestamp=now,
        ip_address=_get_client_ip(),
        status='success',
        notes='Check-in por documento',
        created_by=session.get('user_id')
    )
    db.session.add(entry_log)

    # Crear ActiveSession
    session_row = ActiveSession(
        user_id=user.id,
        entry_time=now,
        status='active'
    )
    db.session.add(session_row)

    # Auditoría
    audit = SystemAudit(
        user_id=session.get('user_id', user.id),
        table_affected='active_sessions',
        action_type='CREATE',
        new_values=f'ENTRY user_id={user.id} at {now.isoformat()}',
        ip_address=_get_client_ip()
    )
    db.session.add(audit)

    db.session.commit()
    return jsonify(success=True, message='Check-in registrado', user_id=user.id, entry_time=now.isoformat())


@attendance_bp.route('/attendance/checkout', methods=['POST'])
def checkout():
    data = request.get_json(silent=True) or request.form
    doc_id = data.get('idDocumento')
    if not doc_id:
        return jsonify(success=False, error='idDocumento requerido'), 400

    user = _find_user_by_document(doc_id)
    if not user:
        return jsonify(success=False, error='Usuario no encontrado'), 404
    if not user.is_active or user.estado_id is None:
        return jsonify(success=False, error='Usuario inactivo'), 403

    # Buscar sesión activa
    active = ActiveSession.query.filter_by(user_id=user.id).filter(ActiveSession.exit_time.is_(None)).first()
    if not active:
        return jsonify(success=False, error='No existe una entrada activa'), 409

    now = _now_utc()
    active.exit_time = now
    active.status = 'closed'

    # AccessLog EXIT
    exit_log = AccessLog(
        user_id=user.id,
        action_type='EXIT',
        timestamp=now,
        ip_address=_get_client_ip(),
        status='success',
        notes='Check-out por documento',
        created_by=session.get('user_id')
    )
    db.session.add(exit_log)

    # Auditoría
    audit = SystemAudit(
        user_id=session.get('user_id', user.id),
        table_affected='active_sessions',
        action_type='UPDATE',
        old_values=f'ENTRY {active.entry_time.isoformat()}',
        new_values=f'EXIT {now.isoformat()}',
        ip_address=_get_client_ip()
    )
    db.session.add(audit)

    db.session.commit()
    return jsonify(success=True, message='Check-out registrado', user_id=user.id, exit_time=now.isoformat())


# Admin views
@attendance_bp.route('/admin/sesiones-activas')
@admin_required
def sesiones_activas():
    page = request.args.get('page', 1, type=int)
    q = ActiveSession.query.join(User, User.id == ActiveSession.user_id) \
        .filter(ActiveSession.exit_time.is_(None)) \
        .add_columns(User) \
        .order_by(ActiveSession.entry_time.desc())
    pagination = q.paginate(page=page, per_page=20, error_out=False)
    now = _now_utc()
    return render_template('admin/sesiones_activas.html', pagination=pagination, now=now)


@attendance_bp.route('/admin/historial-asistencia')
@admin_required
def historial_asistencia():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    start = request.args.get('start')
    end = request.args.get('end')
    tipo = request.args.get('tipo')  # ENTRY/EXIT

    q = AccessLog.query.join(User, User.id == AccessLog.user_id).add_columns(User)

    if search:
        try:
            doc = int(search)
            q = q.filter(or_(User.idDocumento == doc,
                             User.first_name.contains(search),
                             User.last_name.contains(search)))
        except ValueError:
            q = q.filter(or_(User.first_name.contains(search), User.last_name.contains(search)))

    if tipo in ('ENTRY', 'EXIT'):
        q = q.filter(AccessLog.action_type == tipo)

    # Fecha
    def _parse_date(s):
        try:
            return datetime.fromisoformat(s)
        except Exception:
            return None

    if start:
        dt = _parse_date(start)
        if dt:
            q = q.filter(AccessLog.timestamp >= dt)
    if end:
        dt = _parse_date(end)
        if dt:
            q = q.filter(AccessLog.timestamp <= dt)

    q = q.order_by(AccessLog.timestamp.desc())
    pagination = q.paginate(page=page, per_page=25, error_out=False)

    return render_template('admin/historial_asistencia.html', pagination=pagination, search=search, start=start, end=end, tipo=tipo)
