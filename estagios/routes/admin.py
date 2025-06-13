from flask import Blueprint, request, jsonify
from estagios import db
from estagios.models import User, RoleEnum
from flask_login import login_required, current_user
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/criar-admin', methods=['POST'])
@login_required
def criar_admin():
    if current_user.role != RoleEnum.ADMIN:
        return jsonify({'mensagem': 'Acesso negado.'})
    else:
        dados = request.get_json()
        if User.query.filter_by(email = dados.get('email')).first():
            return jsonify({'erro': 'Email já cadastrado'}), 409

        novo_admin = User(
            email = dados.get('email'),
            senha = dados.get('senha'),
            role = RoleEnum.ADMIN
        )
        db.session.add(novo_admin)
        db.session.commit()

        return jsonify({'mensagem': 'Novo admin criado com sucesso'}), 201
