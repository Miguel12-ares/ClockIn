from flask import Blueprint

estado_bp = Blueprint('estado', __name__)

from . import index, show, create, update, delete
