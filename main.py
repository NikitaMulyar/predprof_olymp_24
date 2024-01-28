from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
from form.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

# from consts import rus_periods
# from get_company_info import get_info


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index0.html', title="Главная страница")


@app.route('/companies.txt/<region>')
def all_companies(region):
    if region == "RU":
        return render_template('index2.html', title="Российская биржа")
    return render_template('index.html', title="Американская биржа")


@app.route('/user')
def user():
    return render_template('user.html')


@app.route('/sub')
def sub():
    return render_template('sub.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(500)
def internal_error(error):
    return "<h1>Ты ошибся!</h2>", 500


@app.route('/company_page/<short_comp>')
def company_page(short_comp):
    kwargs = dict()
    kwargs["data"] = [[0, '2023-03-07', 3],
                      [1, '2023-03-05', 2]
                      ]
    file = open("companies.txt", "rt", encoding="utf8")
    comp = file.readlines()
    file.close()
    for el in comp:
        if el.split(":")[1].strip() == short_comp:
            kwargs["short"] = short_comp
            kwargs["long"] = el.split(":")[0]
            break
    kwargs["title"] = kwargs["long"]
    return render_template('company_table.html', **kwargs)


if __name__ == '__main__':
    db_session.global_init("db/database.db")
    app.run(port=8080, host='127.0.0.1')
