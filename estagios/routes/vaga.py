from flask import Blueprint, request, jsonify
from estagios import db
from estagios.models import Vaga, Empresa

vaga_bp = Blueprint('vaga', __name__, url_prefix='/vaga')


@vaga_bp.route('/', methods=['POST'])
def criar_vaga():
    dados = request.get_json()

    empresa = Empresa.query.get(dados.get('empresa_id'))
    if not empresa:
        return jsonify({'erro': 'Empresa não encontrada'}), 404

    try:
        nova_vaga = Vaga(
            empresa_id=dados.get('empresa_id'),
            titulo=dados.get('titulo'),
            valor_bolsa=dados.get('valor_bolsa'),
            descricao=dados.get('descricao'),
            cursos=dados.get('cursos')
        )
        db.session.add(nova_vaga)
        db.session.commit()
        return jsonify({'mensagem': 'Vaga criada com sucesso', 'id': nova_vaga.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@vaga_bp.route('/', methods=['GET'])
def listar_vagas():
    vagas = Vaga.query.all()
    return jsonify([
        {
            'id': vaga.id,
            'titulo': vaga.titulo,
            'valor_bolsa': vaga.valor_bolsa,
            'descricao': vaga.descricao,
            'cursos': vaga.cursos,
            'empresa_id': vaga.empresa_id,
            'data_criacao': vaga.data_criacao.isoformat(),
            'empresa_nome': vaga.empresa.nome
        }
        for vaga in vagas
    ])


@vaga_bp.route('/<int:vaga_id>', methods=['GET'])
def obter_vaga(vaga_id):
    vaga = Vaga.query.get(vaga_id)
    if not vaga:
        return jsonify({'erro': 'Vaga não encontrada'}), 404

    return jsonify({
        'id': vaga.id,
        'titulo': vaga.titulo,
        'valor_bolsa': vaga.valor_bolsa,
        'descricao': vaga.descricao,
        'cursos': vaga.cursos,
        'empresa_id': vaga.empresa_id,
        'data_criacao': vaga.data_criacao.isoformat(),
        'empresa_nome': vaga.empresa.nome
    })

@vaga_bp.route('/<int:vaga_id>', methods=['PUT'])
def atualizar_vaga(vaga_id):
    vaga = Vaga.query.get(vaga_id)
    if not vaga:
        return jsonify({'erro': 'Vaga não encontrada'}), 404

    dados = request.get_json()
    try:
        vaga.titulo = dados.get('titulo', vaga.titulo)
        vaga.valor_bolsa = dados.get('valor_bolsa', vaga.valor_bolsa)
        vaga.descricao = dados.get('descricao', vaga.descricao)
        vaga.cursos = dados.get('cursos', vaga.cursos)
        db.session.commit()
        return jsonify({'mensagem': 'Vaga atualizada com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@vaga_bp.route('/<int:vaga_id>', methods=['DELETE'])
def deletar_vaga(vaga_id):
    vaga = Vaga.query.get(vaga_id)
    if not vaga:
        return jsonify({'erro': 'Vaga não encontrada'}), 404

    try:
        db.session.delete(vaga)
        db.session.commit()
        return jsonify({'mensagem': 'Vaga deletada com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400
