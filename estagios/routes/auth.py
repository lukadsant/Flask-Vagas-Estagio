from estagios import db, mail
from estagios.models import User, RoleEnum
from flask import Blueprint, request, jsonify
from flask_mail import Message
import random 

auth_bp = Blueprint('auth', __name__, url_prefix='auth')


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

@auth_bp.route('/login/estudante', methods=['POST'])
def login_estudante():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    usuario = User.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404

    if usuario.role != RoleEnum.ESTUDANTE:
        return jsonify({'erro': 'Usuário não é estudante'}), 403

    if usuario.senha != senha:
        return jsonify({'erro': 'Senha incorreta'}), 401

    return jsonify({'mensagem': 'Login realizado com sucesso', 'user_id': usuario.id})
