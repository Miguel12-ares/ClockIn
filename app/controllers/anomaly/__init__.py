from flask import Blueprint

anomaly_bp = Blueprint('anomaly', __name__)

from . import index, show, create, resolve
