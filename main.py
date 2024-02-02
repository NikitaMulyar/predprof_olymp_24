from flask import Flask, render_template
from consts import rus_periods
from get_company_info import get_rus_company_info


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/<land_name>')
def get_company(land_name):
    kwargs = dict()
    kwargs['land_name'] = land_name

    return render_template('land_stocks.html', **kwargs)


@app.errorhandler(500)
def internal_error(error):
    return "<h1>Ты ошибся!</h2>", 500


@app.route('/<company_name>/<period>/<int:total>/')
def get_company(company_name, period, total):
    kwargs = dict()
    kwargs['company'] = company_name
    kwargs['total'] = total
    kwargs['period'] = rus_periods[period]

    get_rus_company_info(company_name, period, total)

    return render_template('company_info.html', **kwargs)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
