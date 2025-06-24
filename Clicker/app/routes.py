from flask import Blueprint, render_template, redirect, url_for, flash
from app.extensions import db, bcrypt, login_manager
from app.models import User
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Маршруты аутентификации
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна! Теперь войдите', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# Основные маршруты
@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/click')
@login_required
def click():
    current_user.clicks += 1
    db.session.commit()
    return redirect(url_for('main.index'))
