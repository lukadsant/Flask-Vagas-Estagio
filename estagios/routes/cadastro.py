from estagios import db
from estagios.models import User
from flask import Blueprint, request, jsonify

cadastro_bp = Blueprint('cadastro', __name__, url_prefix='cadastro')
@cadastro_bp.route('/cadastro', methods=['POST'])
def cadastro():
    dados = request.json
    novo_usuario = User(
        email = dados.get('email'),
        senha = dados.get('senha'),
        role = dados.get('role')
    )
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({
        'mensagem': 'Usuário criado com sucesso'
    }), 400

