from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.models.user_type import UserType

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    data = request.get_json() if request.is_json else request.form
    id_documento = data.get('idDocumento')
    password = data.get('password')

    if not id_documento or not password:
        if request.is_json:
            return jsonify({'error': 'ID y contraseña requeridos'}), 400
        flash('ID y contraseña requeridos', 'error')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(idDocumento=id_documento, is_active=True).first()

    if user and user.check_password(password):
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'user_type_id': user.user_type_id,
                'zona_id': user.zona_id,
                'user_type_name': user.user_type.type_name
            }
        )

        if request.is_json:
            return jsonify({
                'access_token': access_token,
                'user_type': user.user_type.type_name,
                'zona_id': user.zona_id
            })

        session['user_id'] = user.id
        session['user_type'] = user.user_type.type_name
        return redirect(url_for('main.dashboard'))

    if request.is_json:
        return jsonify({'error': 'Credenciales inválidas'}), 401
    flash('Credenciales inválidas', 'error')
    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
