from flask import Blueprint
from flask import request, jsonify
from estagios import db
from estagios.models import User
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['POST', 'GET'])
def admin_home():
    return 'Olá'