from flask import jsonify, request
from app.controllers.system_audit import system_audit_bp
from app.models.system_audit import SystemAudit
from app import db

@system_audit_bp.route('/<int:audit_id>', methods=['GET'])
def show(audit_id):
    """
    Obtiene una auditoría específica por ID
    """
    try:
        audit = SystemAudit.query.get(audit_id)
        
        if not audit:
            return jsonify({
                'success': False,
                'error': 'Auditoría no encontrada',
                'message': f'No existe una auditoría con ID {audit_id}'
            }), 404
        
        # Obtener información relacionada
        audit_data = {
            'id': audit.id,
            'user': {
                'id': audit.user.id,
                'idDocumento': audit.user.idDocumento,
                'first_name': audit.user.first_name,
                'last_name': audit.user.last_name,
                'user_type': audit.user.user_type.type_name if audit.user.user_type else None,
                'zona': {
                    'id': audit.user.zona.id,
                    'sede_nombre': audit.user.zona.sede_nombre,
                    'departamento': audit.user.zona.departamento,
                    'ciudad': audit.user.zona.ciudad
                } if audit.user.zona else None,
                'estado': audit.user.estado.name if audit.user.estado else None,
                'is_active': audit.user.is_active
            } if audit.user else None,
            'table_affected': audit.table_affected,
            'action_type': audit.action_type,
            'old_values': audit.old_values,
            'new_values': audit.new_values,
            'timestamp': audit.timestamp.isoformat() if audit.timestamp else None,
            'ip_address': audit.ip_address
        }
        
        return jsonify({
            'success': True,
            'data': audit_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
