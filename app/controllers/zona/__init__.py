from flask import Blueprint

zona_bp = Blueprint('zona', __name__)

from . import index, show, create, update, delete
