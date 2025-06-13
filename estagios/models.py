from . import db
from datetime import datetime
import enum
from flask_login import UserMixin

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
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)

    # # Relação 1:1 com Empresa (se o usuário for empresa)
    # empresa = db.relationship('Empresa', backref='user', uselist=False)

    # Relação 1:1 com Estudante (se o usuário for estudante)
    estudante = db.relationship('Estudante', backref='user', uselist=False)

# Empresa (relacionada 1:1 com User e 1:N com Vaga)
class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) empresa não vai ser mais um usuario
    CNPJ = db.Column(db.String(20), unique=True, nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    # liberada = db.Column(db.Boolean, default=False) acho que não vai precisar mais
    telefone = db.Column(db.String(20), nullable=False)
    email = email = db.Column(db.String(120), unique=True, nullable=False)
    # Uma empresa pode ter várias vagas
    vagas = db.relationship('Vaga', backref='empresa', lazy=True)

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
