from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import dotenv_values
from flask_login import LoginManager


app = Flask(__name__)
app.config.update(dotenv_values('estagios/.env'))
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

with app.app_context():
    from estagios.models import User, RoleEnum
    if not User.query.filter_by(email='xavierbruna9@gmail.com').first():
        admin = User(email='xavierbruna9@gmail.com', senha='123456', role=RoleEnum.ADMIN)
        db.session.add(admin)
        db.session.commit()
        print("Admin criado")