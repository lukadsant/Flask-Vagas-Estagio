from flask import Blueprint
from flask import request, jsonify
from estagios import db
from estagios.models import User, Estudante
estudante_bp = Blueprint('estudante', __name__, url_prefix='/estudante')

@estudante_bp.route('/', methods=['POST', 'GET'])
def estudante_home():
    return 'Olá'