from flask import Blueprint
from flask import request, jsonify
from estagios import db
from estagios.models import User, candidatura
candidatura_bp = Blueprint('candidatura', __name__, url_prefix='/candidatura')

@candidatura_bp.route('/home', methods=['POST', 'GET'])
def candidatura_home():
    return 'Olá'