from flask import Blueprint

access_log_bp = Blueprint('access_log', __name__)

from . import index, show, create
