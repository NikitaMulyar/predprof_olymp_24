from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

# from consts import rus_periods
# from get_company_info import get_info


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


class LoginForm(FlaskForm):
    user_id = StringField('login', validators=[DataRequired()])
    user_password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index (1).html')


@app.route('/user')
def user():
    return render_template('user.html')


@app.route('/sub')
def sub():
    return render_template('sub.html')


# @app.route('/login')
# def log():
#     return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/user')
    return render_template('login.html', title='Авторизация', form=form)


# @app.route('/<land_name>')
# def get_company(land_name):
#     kwargs = dict()
#     kwargs['land_name'] = land_name
#
#     return render_template('land_stocks.html', **kwargs)
#
@app.route('/reg')
def reg():
    return render_template('reg.html')
@app.errorhandler(500)
def internal_error(error):
    return "<h1>Ты ошибся!</h2>", 500


#
# @script.route('/<company_name>/<period>/<int:total>/')
# def get_company(company_name, period, total):
#     kwargs = dict()
#     kwargs['company'] = company_name
#     kwargs['total'] = total
#     kwargs['period'] = rus_periods[period]
#
#     get_info(company_name, period, total)
#
#     return render_template('company_info.html', **kwargs)

@app.route('/company_page')
def company_page():
    return render_template('company_table.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
