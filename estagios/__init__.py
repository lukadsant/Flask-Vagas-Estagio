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

from .routes.admin import admin_bp
from .routes.empresa import empresa_bp
from .routes.estudante import estudante_bp
from .routes.vaga import vaga_bp
from .routes.candidatura import candidatura_bp
from .routes.auth import auth_bp

app.register_blueprint(admin_bp)
app.register_blueprint(empresa_bp)
app.register_blueprint(estudante_bp)
app.register_blueprint(vaga_bp)
app.register_blueprint(candidatura_bp)
app.register_blueprint(auth_bp)
