from flask import jsonify, request
from app.controllers.estado import estado_bp
from app.models.estado import Estado
from app import db

@estado_bp.route('/', methods=['POST'])
def create():
    """
    Crea un nuevo estado
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para crear el estado'
            }), 400
        
        # Validar campos requeridos
        if 'name' not in data or not data['name']:
            return jsonify({
                'success': False,
                'error': 'Campo requerido faltante',
                'message': 'El campo name es requerido'
            }), 400
        
        # Verificar si ya existe un estado con el mismo nombre
        existing_estado = Estado.query.filter_by(name=data['name']).first()
        if existing_estado:
            return jsonify({
                'success': False,
                'error': 'Estado duplicado',
                'message': f'Ya existe un estado con el nombre {data["name"]}'
            }), 400
        
        # Crear nuevo estado
        new_estado = Estado(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(new_estado)
        db.session.commit()
        
        # Retornar estado creado
        estado_data = {
            'id': new_estado.id,
            'name': new_estado.name,
            'description': new_estado.description,
            'users_count': 0
        }
        
        return jsonify({
            'success': True,
            'message': 'Estado creado exitosamente',
            'data': estado_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
