from flask import Blueprint

admin_zona_bp = Blueprint('admin_zona', __name__)

from . import assign, remove, list
