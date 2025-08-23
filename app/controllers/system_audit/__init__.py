from flask import Blueprint

system_audit_bp = Blueprint('system_audit', __name__)

from . import index, show
