from flask import Blueprint
from flask import request, jsonify
from estagios import db
from estagios.models import User, Vaga
vaga_bp = Blueprint('vaga', __name__, url_prefix='/vaga')

@vaga_bp.route('/', methods=['POST', 'GET'])
def vaga_home():
    return 'Olá'