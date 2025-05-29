from flask import Blueprint
from flask import request
from estagios import db
from estagios.models import User, RoleEnum, Estudante, Empresa
Empresa_bp = Blueprint('empresa', __name__, url_prefix='/empresa')

@Empresa_bp.route('/cadastra_empresa', methods=['POST'])
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