
# API Sistema de Cadastro de Empresas Parceiras

A API do Sistema de Cadastro de Empresas Parceiras foi desenvolvida para facilitar a integração entre administradores, empresas e alunos do IFPE Campus Jaboatão. Ela fornece endpoints RESTful que permitem o gerenciamento de empresas, publicação de vagas e candidaturas de estudantes de forma centralizada e organizada.


## Funcionalidades

- Cadastro e gerenciamento de empresas parceiras
- Criação, listagem e remoção de vagas vinculadas às empresas
- Registro de alunos e envio de candidaturas às vagas disponíveis
- Listagem pública de vagas para acesso livre pelos estudantes


## Stack utilizada

**Back-end:** Python, Flask


## Contribuindo com o Projeto

Criando o ambiente virtual e instalando dependências

```bash
  python -m venv myvenv
  . myvenv/Scripts/activate (ativando)
  pip install requirements.txt
```
Salvando novas dependências no requirements.txt

```bash
  pip freeze > requirements.txt (dentro do seu ambiente virtual)
```
Estrutura do Projeto

```
Flask-Vagas-Estagio/
├── estagios/
│   ├── __pycache__/
│   ├── routes/
│   │   └── __init__.py
│   ├── models.py
│   ├── rotas.py
│   └── .env          ← Arquivo de variáveis de ambiente (colocar aqui)
├── instance/
├── venv/             ← Ambiente virtual (criar na raiz do projeto)
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
```
## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

`SQLALCHEMY_DATABASE_URI`

`SQLALCHEMY_TRACK_MODIFICATIONS`

`MAIL_SERVER`

`MAIL_PORT`

`MAIL_USERNAME`

`MAIL_PASSWORD`

`MAIL_USE_TLS`