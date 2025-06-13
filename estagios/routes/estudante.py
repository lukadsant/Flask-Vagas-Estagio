from flask import Blueprint, request, jsonify
from estagios import db
from estagios.models import Estudante, User, RoleEnum
from flask_login import login_required, current_user

estudante_bp = Blueprint('estudante', __name__, url_prefix='/estudante')

@estudante_bp.route('/complementar', methods=['POST'])
def cadastrar_dados_complementares():
    dados = request.get_json()
    user_id = dados.get('user_id')

    usuario = User.query.get(user_id)
    if not usuario or usuario.role != RoleEnum.ESTUDANTE:
        return jsonify({'erro': 'Usuário inválido ou não é estudante'}), 400

    if Estudante.query.filter_by(user_id=user_id).first():
        return jsonify({'erro': 'Dados complementares já cadastrados'}), 409

    estudante = Estudante(
        user_id=user_id,
        user_email=usuario.email,
        nome=dados.get('nome'),
        curriculo_profissional_link=dados.get('curriculo_profissional_link'),
        telefone=dados.get('telefone'),
        curso=dados.get('curso'),
        periodo=dados.get('periodo')
    )
    db.session.add(estudante)
    db.session.commit()

    return jsonify({'mensagem': 'Cadastro complementar realizado com sucesso'}), 201


@estudante_bp.route('/<int:user_id>', methods=['GET'])
def pegar_dados_estudante(user_id):
    estudante = Estudante.query.filter_by(user_id=user_id).first()
    if not estudante:
        return jsonify({'erro': 'Dados do estudante não encontrados'}), 404

    return jsonify({
        'nome': estudante.nome,
        'curriculo_profissional_link': estudante.curriculo_profissional_link,
        'telefone': estudante.telefone,
        'curso': estudante.curso,
        'periodo': estudante.periodo
    })

@estudante_bp.route('/<int:user_id>', methods=['PUT'])
@login_required
def atualizar_dados_estudante(user_id):
    if current_user.role != RoleEnum.ESTUDANTE:
        return jsonify({'mensagem': 'Acesso negado'})
    else:
        estudante = Estudante.query.filter_by(user_id=user_id).first()
        if not estudante:
            return jsonify({'erro': 'Dados do estudante não encontrados'}), 404

        dados = request.get_json()
        estudante.nome = dados.get('nome', estudante.nome)
        estudante.curriculo_profissional_link = dados.get('curriculo_profissional_link', estudante.curriculo_profissional_link)
        estudante.telefone = dados.get('telefone', estudante.telefone)
        estudante.curso = dados.get('curso', estudante.curso)
        estudante.periodo = dados.get('periodo', estudante.periodo)

        db.session.commit()

        return jsonify({'mensagem': 'Dados atualizados com sucesso'})


@estudante_bp.route('/<int:user_id>', methods=['DELETE'])
@login_required
def excluir_dados_estudante(user_id):
    if current_user.role != RoleEnum.ESTUDANTE:
        return jsonify({'mensagem': 'Acesso negado'})
    else:
        estudante = Estudante.query.filter_by(user_id=user_id).first()
        if not estudante:
            return jsonify({'erro': 'Dados do estudante não encontrados'}), 404

        db.session.delete(estudante)
        db.session.commit()

        return jsonify({'mensagem': 'Dados do estudante excluídos com sucesso'})
