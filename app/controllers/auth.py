from flask import Blueprint, render_template, request
from app.models.user import User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Lógica de login por ID (inyección de db)
    if request.method == 'POST':
        # Validar y autenticar
        pass
    return render_template('login.html')
