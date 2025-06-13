from estagios import db
from datetime import datetime
import enum

# Enum para tipos de usuário
class RoleEnum(enum.Enum):
    ADMIN = "admin"
    EMPRESA = "empresa"
    ESTUDANTE = "estudante"

# Tabela associativa para candidaturas (N:N entre Estudante e Vaga)
candidatura = db.Table('candidatura',
    db.Column('estudante_id', db.Integer, db.ForeignKey('estudante.id'), primary_key=True),
    db.Column('vaga_id', db.Integer, db.ForeignKey('vaga.id'), primary_key=True)
)

# Usuário base
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)

    # Relação 1:1 com Empresa (se o usuário for empresa)
    empresa = db.relationship('Empresa', backref='user', uselist=False)

    # Relação 1:1 com Estudante (se o usuário for estudante)
    estudante = db.relationship('Estudante', backref='user', uselist=False)

# Empresa (relacionada 1:1 com User e 1:N com Vaga)
from flask import Blueprint, request, jsonify
from estagios import db
from estagios.models import Empresa, User, RoleEnum

empresa_bp = Blueprint('empresa', __name__, url_prefix='/empresa')

def checar_admin(user_id):
    usuario = User.query.get(user_id)
    if not usuario or usuario.role != RoleEnum.ADMIN:
        return False
    return True

@empresa_bp.route('', methods=['POST'])
def criar_empresa():
    dados = request.get_json()
    user_id = dados.get('user_id')

    if not checar_admin(user_id):
        return jsonify({'erro': 'Permissão negada'}), 403

    if Empresa.query.filter_by(cnpj=dados.get('cnpj')).first():
        return jsonify({'erro': 'Empresa com esse CNPJ já existe'}), 409

    empresa = Empresa(
        nome=dados.get('nome'),
        cnpj=dados.get('cnpj'),
        endereco=dados.get('endereco'),
        # demais campos...
    )
    db.session.add(empresa)
    db.session.commit()

    return jsonify({'mensagem': 'Empresa criada com sucesso'}), 201

@empresa_bp.route('/<int:id>', methods=['GET'])
def pegar_empresa(id):
    empresa = Empresa.query.get(id)
    if not empresa:
        return jsonify({'erro': 'Empresa não encontrada'}), 404

    return jsonify({
        'nome': empresa.nome,
        'cnpj': empresa.cnpj,
        'endereco': empresa.endereco,
        # demais campos...
    })

@empresa_bp.route('/<int:id>', methods=['PUT'])
def atualizar_empresa(id):
    dados = request.get_json()
    user_id = dados.get('user_id')

    if not checar_admin(user_id):
        return jsonify({'erro': 'Permissão negada'}), 403

    empresa = Empresa.query.get(id)
    if not empresa:
        return jsonify({'erro': 'Empresa não encontrada'}), 404

    empresa.nome = dados.get('nome', empresa.nome)
    empresa.cnpj = dados.get('cnpj', empresa.cnpj)
    empresa.endereco = dados.get('endereco', empresa.endereco)
    # demais campos...

    db.session.commit()
    return jsonify({'mensagem': 'Empresa atualizada com sucesso'})

@empresa_bp.route('/<int:id>', methods=['DELETE'])
def deletar_empresa(id):
    dados = request.get_json()
    user_id = dados.get('user_id')

    if not checar_admin(user_id):
        return jsonify({'erro': 'Permissão negada'}), 403

    empresa = Empresa.query.get(id)
    if not empresa:
        return jsonify({'erro': 'Empresa não encontrada'}), 404

    db.session.delete(empresa)
    db.session.commit()
    return jsonify({'mensagem': 'Empresa deletada com sucesso'})


# Estudante (relacionado 1:1 com User e N:N com Vaga)
class Estudante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    curriculo_profissional_link = db.Column(db.String(200))
    telefone = db.Column(db.String(20), nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    periodo = db.Column(db.String(20), nullable=False)

    # Relação muitos-para-muitos com Vaga (candidaturas)
    vagas = db.relationship('Vaga', secondary='candidatura', backref=db.backref('estudantes', lazy='dynamic'))

# Vaga de estágio
class Vaga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    valor_bolsa = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    cursos = db.Column(db.String(200), nullable=False)  # Ex: "Administração,Engenharia"
