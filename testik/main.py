from flask import Flask, render_template
from moexalgo import Ticker
import pandas as pd
from datetime import date, timedelta, datetime
import csv


app = Flask(__name__)
PERIODS = {'D': 'дней', 'W': 'недель'}


def get_info(company, period, total):
    periods = {'weeks': total if period == 'W' else 0,
               'days': total if period == 'D' else 0
               }
    tick = Ticker(company)
    today = date.today()
    df = pd.DataFrame(tick.candles(date=today - timedelta(**periods), till_date=today, period=period))
    df = df[['begin', 'open', 'close', 'high', 'low', 'value', 'volume', 'end']]
    df.rename(columns={'volume': 'quantity'})
    df = df[['begin', 'open', 'close']]
    df.to_csv(f'csv_files/{company}.csv')


@app.route('/')
@app.route('/index')
def index():
    return render_template('usa.html')


@app.errorhandler(500)
def internal_error(error):
    return "<h1>Ты ошибся!</h2>", 500


@app.route('/<company_name>/<period>/<int:total>/')
def get_company(company_name, period, total):
    kwargs = dict()
    kwargs['company'] = company_name
    kwargs['total'] = total
    kwargs['period'] = PERIODS[period]
    get_info(company_name, period, total)
    kwargs['data'] = []
    with open(f'csv_files/{company_name}.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        title = next(reader)
        for i, row in enumerate(reader):
            kwargs['data'].append(row[1:])
    kwargs['data'] = kwargs['data'][::-1]
    return render_template('company_info.html', **kwargs)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
