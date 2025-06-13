from estagios import db, mail
from estagios.models import User, RoleEnum
from flask import Blueprint, request, jsonify
from flask_mail import Message
import random 
from flask_login import login_user, logout_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/cadastro', methods=['POST'])
def cadastro_usuario():
    dados = request.json
    novo_usuario = User(
        email = dados.get('email'),
        senha = dados.get('senha'),
        role = RoleEnum(dados.get('role'))
    )
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({
        'mensagem': 'Usuário criado com sucesso'
    })

@auth_bp.route('/confirmar-email', methods=['POST'])
def confirmar_email():
    dados = request.get_json()
    id = dados.get('id')
    codigo = ''.join(random.choice('0123456789') for _ in range(6))
    usuario = User.query.get(id)
    msg = Message(
                subject = "Olá, confirme seu email.",
                body = f"Seu código de confirmação: {codigo}",
                sender = ('Estágio Parceiro | IFPE','estagioparceiro@gmail.com'),
                recipients = [usuario.email]
            )
    mail.send(msg)
    return jsonify({'mensagem': 'Email enviado com sucesso.', 'codigo': codigo})

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    user = User.query.filter_by(email=email).first()

    if not user or user.senha != senha:
        return jsonify({'erro': 'Credenciais inválidas'}), 401

    login_user(user)  # cria a sessão
    return jsonify({'mensagem': 'Login bem-sucedido', 'user_id': user.id})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'mensagem': 'Logout efetuado com sucesso'})