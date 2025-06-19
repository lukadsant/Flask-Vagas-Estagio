from flask import Blueprint, request, jsonify
from flask_mail import Message
from estagios import db
from estagios.models import Estudante, Vaga

candidatura_bp = Blueprint('candidatura', __name__, url_prefix='/candidatura')

# Criar candidatura (estudante se candidata a uma vaga)
@candidatura_bp.route('/candidatura', methods=['POST'])
def criar_candidatura():
    dados = request.get_json()
    estudante_id = dados.get('estudante_id')
    vaga_id = dados.get('vaga_id')

    estudante = Estudante.query.get(estudante_id)
    vaga = Vaga.query.get(vaga_id)

    if not estudante or not vaga:
        return jsonify({'erro': 'Estudante ou vaga não encontrada'}), 404

    if vaga in estudante.vagas:
        return jsonify({'erro': 'Estudante já se candidatou a essa vaga'}), 409

    estudante.vagas.append(vaga)
    db.session.commit()

    # Enviar e-mail de confirmação
    try:
        msg = Message(
            subject="Candidatura Confirmada - Estágio Parceiro",
            sender=("Estágio Parceiro | IFPE", "estagioparceiro@gmail.com"),
            recipients=[estudante.user_email],
            body=f"""
Olá, {estudante.nome}!

Você se candidatou com sucesso à vaga "{vaga.titulo}".

Seu currículo foi encaminhado à empresa. Link informado:
{estudante.curriculo_profissional_link}

Boa sorte!

Equipe Estágio Parceiro | IFPE
            """
        )
        mail.send(msg)
    except Exception as e:
        return jsonify({'mensagem': 'Candidatura criada, mas o envio do e-mail falhou.', 'erro': str(e)}), 500

    return jsonify({'mensagem': 'Candidatura realizada com sucesso. E-mail enviado.'}), 201


# Listar vagas que um estudante se candidatou
@candidatura_bp.route('/estudante/<int:estudante_id>', methods=['GET'])
def listar_candidaturas_estudante(estudante_id):
    estudante = Estudante.query.get(estudante_id)
    if not estudante:
        return jsonify({'erro': 'Estudante não encontrado'}), 404

    return jsonify([
        {
            'vaga_id': vaga.id,
            'titulo': vaga.titulo,
            'descricao': vaga.descricao,
            'valor_bolsa': vaga.valor_bolsa
        } for vaga in estudante.vagas
    ])

# Listar estudantes que se candidataram a uma vaga
@candidatura_bp.route('/vaga/<int:vaga_id>', methods=['GET'])
def listar_candidatos_vaga(vaga_id):
    vaga = Vaga.query.get(vaga_id)
    if not vaga:
        return jsonify({'erro': 'Vaga não encontrada'}), 404

    return jsonify([
        {
            'estudante_id': est.id,
            'nome': est.nome,
            'curso': est.curso,
            'email': est.user_email
        } for est in vaga.estudantes
    ])

# Remover candidatura
@candidatura_bp.route('/', methods=['DELETE'])
def remover_candidatura():
    dados = request.get_json()
    estudante_id = dados.get('estudante_id')
    vaga_id = dados.get('vaga_id')

    estudante = Estudante.query.get(estudante_id)
    vaga = Vaga.query.get(vaga_id)

    if not estudante or not vaga:
        return jsonify({'erro': 'Estudante ou vaga não encontrada'}), 404

    if vaga not in estudante.vagas:
        return jsonify({'erro': 'Candidatura não encontrada'}), 400

    estudante.vagas.remove(vaga)
    db.session.commit()
    return jsonify({'mensagem': 'Candidatura removida com sucesso'})
