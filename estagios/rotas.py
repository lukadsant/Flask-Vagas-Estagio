from estagios import app, mail
from flask import request
import random
from flask_mail import Message
from estagios import db
from estagios.models import User, RoleEnum, Estudante, Empresa


@app.route('/')
def homepage():
    return "Home Page"

@app.route('/cadastra_usuario', methods=['POST'])
def cadastraUsuario():
    dados = request.get_json()
    novoUsuario = User(
        email = dados.get('email'),
        senha = dados.get('senha'),
        role = RoleEnum(dados.get('role'))
    )
    db.session.add(novoUsuario)
    db.session.commit()
    return {'id': novoUsuario.id}

@app.route('/confirma_email', methods=['POST'])
def confirmaEmail():
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
    return f"Mensagem enviada para: {usuario.email}"


@app.route('/cadastra_estudante', methods=['POST'])
def cadastraEstudante():
    dados = request.get_json()
    usuario = User.query.get(dados.get('id'))
    novoEstudante = Estudante(
        user_id = usuario.id,
        user_email = usuario.email,
        nome = dados.get('nome'),
        curriculo_profissional_link = dados.get('curriculo'),
        telefone = dados.get('telefone'),
        curso = dados.get('curso'),
        periodo = dados.get('periodo')
    )
    db.session.add(novoEstudante)
    db.session.commit()
    return {'id': novoEstudante.id, 'user_id': novoEstudante.user_id}


@app.route('\cadastra_empresa', methods=['POST'])
def cadastraEmpresa():
    dados = request.get_json()
    usuario = User.query.get(dados.get('id'))
    novaEmpresa = Empresa(
        user_id = usuario.id,
        CNPJ = dados.get('cnpj'),
        endereco = dados.get('endereco'),
        descricao = dados.get('descricao'),
        telefone = dados.get('telefone')
    )
    db.session.add(novaEmpresa)
    db.session.commit()
    return {'id': novaEmpresa.id, 'user_id': usuario.id}