import moexalgo
from moexalgo import Ticker
import pandas as pd
from datetime import date, timedelta
from consts import moex_periods, yfinances_periods
import yfinance as yf


def get_info(company, period, total):
    minutes = 0
    if period == 'MIN':
        minutes = total
    elif period == 'H':
        minutes = total * 60
    elif period == 'D':
        minutes = total * 60 * 24
    elif period == 'W':
        minutes = total * 60 * 24 * 7
    elif period == 'M':
        minutes = total * 60 * 24 * 30
    elif period == 'Q':
        minutes = total * 60 * 24 * 92
    tick = Ticker(company)
    """import pprint
    pprint.pprint(tick.info())
    return"""
    today = date.today()
    fromday = today - timedelta(minutes=minutes) - timedelta(minutes=60 * 24 * 95 * 10)  # Вычитаем квартал
    df = pd.DataFrame(tick.candles(date=fromday, till_date=today, period=moex_periods[period]))
    df = df[len(df) - total:]
    df = df[['begin', 'open', 'close', 'high', 'low']]
    df.set_index('begin', inplace=True)
    df.to_csv(f'csv_files/{company}.csv')


def get_usa_company_info(company, period, total):
    tick = yf.Ticker(company)
    """import pprint
    pprint.pprint(tick.get_info()['longBusinessSummary'])
    return"""
    df = tick.history(interval=yfinances_periods[period], period="max")
    df = df.tail(total)
    df.columns = [x.lower() for x in df.columns]
    df = df[['open', 'close', 'high', 'low']]
    df[['open', 'close', 'high', 'low']] = df[['open', 'close', 'high', 'low']].apply(lambda x: round(x, 2))
    df['begin'] = df.index.values
    df['begin'] = df['begin'].apply(lambda t: t.date())
    df.set_index('begin', inplace=True)
    df.to_csv(f'csv_files/{company}.csv')


if __name__ == '__main__':
    """get_info('KUBE', 'D', 500)
    get_info('LKOH', 'D', 500)
    get_info('MOEX', 'D', 500)
    get_info('SBER', 'D', 500)
    get_info('TCSG', 'D', 500)
    get_info('AFLT', 'D', 500)
    get_info('YNDX', 'D', 500)"""
    """get_usa_company_info("META", 'D', 500)
    get_usa_company_info("AAPL.txt", 'D', 500)
    get_usa_company_info("TSLA", 'D', 500)
    get_usa_company_info("NKE", 'D', 500)
    get_usa_company_info("AIR.F", 'D', 500)
    get_usa_company_info("BA", 'D', 500)
    get_usa_company_info("SBUX", 'D', 500)"""
    get_usa_company_info('DOGE-USD', 'D', 500)
