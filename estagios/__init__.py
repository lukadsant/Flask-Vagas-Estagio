from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import dotenv_values


app = Flask(__name__)
app.config.update(dotenv_values('estagios/.env'))
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .routes.empresa import Empresa_bp
app.register_blueprint(Empresa_bp)

from estagios.rotas import homepage
from estagios.rotas import confirmaEmail
from estagios.rotas import cadastraUsuario
from estagios.rotas import cadastraEstudante