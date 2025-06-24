from flask import Flask
from app.extensions import db, bcrypt, login_manager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '/eBd2M9vN6WPErobBDGmwQ==VxSJWAo80OYreIhM'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clicker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация расширений
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Указываем endpoint для входа

    # Регистрация Blueprint
    from app.routes import auth, main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
