from flask import Blueprint

user_type_bp = Blueprint('user_type', __name__)

from . import index, show, create, update, delete
