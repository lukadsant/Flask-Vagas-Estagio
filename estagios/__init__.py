from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'estagioparceiro@gmail.com'
app.config['MAIL_PASSWORD'] = 'wqxh xzvv xauw eyfw'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .routes.empresa import Empresa_bp
app.register_blueprint(Empresa_bp)

from estagios.rotas import homepage
from estagios.rotas import confirmaEmail
from estagios.rotas import cadastraUsuario
from estagios.rotas import cadastraEstudante