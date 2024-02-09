import csv
import datetime

from flask import Flask, render_template, redirect, abort, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from data import db_session, csv_api
from data.users import User
from data.companies import Company
from data.lands import Land
from data.user_to_company import UserCompany
from form.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import get_company_info
from strategy.absorption import forecast


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    data = []
    for el in db_sess.query(Company).all():
        data.append([el.short_name, el.full_name, el.land.name])
    db_sess.close()
    return render_template('index0.html', massiv=data)


@app.route('/companies/<region>')
def all_companies(region):
    db_sess = db_session.create_session()
    data0 = db_sess.query(Company).join(Land).filter(Land.name == region).all()
    db_sess.close()
    if not data0:
        return abort(500)
    data = []
    for el in data0:
        data.append([el.short_name, el.full_name, el.pic_url, el.description[:200] + '...'])
    if region == 'RUS':
        title = 'Российские компании'
    elif region == 'USA':
        title = 'Иностранные компании'
    else:
        title = 'Криптовалюты'
    return render_template('region_companies.html', massiv=data, title=title)


@app.route('/user')
def user():
    db_sess = db_session.create_session()
    related_companies = db_sess.query(UserCompany).filter(UserCompany.user_id == current_user.id).all()
    all_companies = []
    for elem in related_companies:
        all_companies.append(db_sess.query(Company).filter(Company.id == elem.company_id).first())
    return render_template('user.html', all_companies=all_companies)


@app.route('/sub')
def sub():
    return render_template('sub.html')


@app.route('/<method>/<company>/<int:user_id>')
def add_company_func(method, company, user_id):
    if method not in ['add', 'remove']:
        return render_template('company_added.html', text='Страница не найдена.', res=-1)
    if not current_user.is_authenticated or current_user.id != user_id:
        return render_template('company_added.html', text='Некорректный id.', res=-1)
    db_sess = db_session.create_session()
    check_user = db_sess.query(User).filter(User.id == user_id).first()
    if not check_user:
        return render_template('company_added.html', text='Такого юзера нет.', res=-1)
    check_company = db_sess.query(Company).filter(Company.short_name == company).first()
    if not check_company:
        return render_template('company_added.html', text='Такой компании нет.', res=-1)
    check_exists_relation = db_sess.query(UserCompany).filter((UserCompany.company_id == check_company.id) &
                                                              (UserCompany.user_id == user_id)).first()
    if method == 'add':
        if check_exists_relation:
                return render_template('company_added.html', text='Данная компания уже есть в избранном.', res=-1)
        relation = UserCompany(user_id=user_id, company_id=check_company.id)
        db_sess.add(relation)
        db_sess.commit()
        db_sess.close()
        return render_template('company_added.html', text='Компания добавлена успешно!', res=0)
    db_sess.delete(check_exists_relation)
    db_sess.commit()
    db_sess.close()
    return render_template('company_added.html', text='Компания успешно удалена!', res=0)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        db_sess.close()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
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
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    q = db_sess.query(User).get(user_id)
    db_sess.close()
    return q


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(500)
@app.errorhandler(404)
def internal_error(error):
    return "<h1>Ты ошибся!</h2>", 500


@app.route('/company_page/<name>/<period>/<int:total>', methods=['GET', 'POST'])
def company_page(name, period, total):
    if request.method == 'POST':
        period = period
        total = total
        if request.form['period'] != 'Выберете период':
            period = request.form['period'][0]
        if request.form['total'] != '':
            total = int(request.form['total'])
            if total < 30:
                total = 30
        return redirect(f'/company_page/{name}/{period}/{total}')
    if total < 30:
        total = 30
    db_sess = db_session.create_session()
    comp = db_sess.query(Company).filter(Company.short_name == name).first()
    db_sess.close()
    if comp:
        if comp.land.name == 'RUS':
            get_company_info.get_rus_company_info(comp.short_name, period, total)
        else:
            get_company_info.get_usa_company_info(comp.short_name, period, total)

        table_data = []
        with open(f'csv_files/{name}.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            t = next(reader)
            for index, row in enumerate(reader):
                table_data.append(row)
        csvfile.close()

        res = forecast(total, name)
        buy_data = []
        sell_data = []
        edata = []
        with open(f'strategy_results/{name}.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            t = next(reader)
            for index, row in enumerate(reader):
                d = {"date": row[0], "price": float(row[-1]), "count": int(row[-2]),
                     "bought": row[1] == 'True'}
                if row[1] == 'True':
                    buy_data.append([row[0], float(row[-1]), int(row[-2])])
                else:
                    sell_data.append([row[0], float(row[-1]), int(row[-2])])
                edata.append(d)
        csvfile.close()

        return render_template('company_table.html', pic_url=comp.pic_url,
                               company=comp.short_name, description=comp.description,
                               full_company_name=comp.full_name, buy_data=buy_data, table_data=table_data,
                               sell_data=sell_data, edata=edata, res=res)
    return abort(404)


if __name__ == '__main__':
    db_session.global_init("db/database.db")
    app.register_blueprint(csv_api.blueprint)
    app.run(port=5000, host='127.0.0.1')
