from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, current_user, login_required, login_user
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ваш_секретный_ключ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Указываем endpoint для страницы входа


# Заглушка для примера (в реальном проекте замените на запрос к БД)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Форма редактирования профиля
class EditProfileForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Новый пароль (оставьте пустым, если не меняется)')
    confirm_password = PasswordField('Повторите пароль', validators=[
        EqualTo('password', message='Пароли должны совпадать!')
    ])
    submit = SubmitField('Сохранить')


# Главная страница
@app.route('/')
def home():
    return """
        <h1>Главная страница</h1>
        <a href="/edit_profile">Редактировать профиль</a>
        <br>
        <a href="/login">Войти</a>
    """


# Страница входа (заглушка для примера)
@app.route('/login')
def login():
    user = User.query.first()  # Для теста берём первого пользователя
    login_user(user)
    flash('Вы успешно вошли!', 'success')
    return redirect(url_for('home'))


# Страница профиля
@app.route('/profile')
@login_required
def profile():
    return f"""
        <h1>Профиль</h1>
        <p>Имя: {current_user.username}</p>
        <p>Email: {current_user.email}</p>
        <a href="/edit_profile">Редактировать</a>
    """


# Редактирование профиля
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.password.data:
            current_user.set_password(form.password.data)

        db.session.commit()
        flash('Профиль успешно обновлён!', 'success')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Создаём тестового пользователя, если его нет
        if not User.query.first():
            user = User(username="admin", email="admin@example.com")
            user.set_password("12345")
            db.session.add(user)
            db.session.commit()

    app.run(debug=True)
