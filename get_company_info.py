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
    today = date.today()
    fromday = today - timedelta(minutes=minutes) - timedelta(minutes=60 * 24 * 95 * 10)  # Вычитаем квартал
    df = pd.DataFrame(tick.candles(date=fromday, till_date=today, period=moex_periods[period]))
    df = df[:total]
    df = df[['begin', 'open', 'close', 'high', 'low']]
    df.set_index('begin', inplace=True)
    df.to_csv(f'csv_files/{company}.csv')


def get_usa_company_info(company, period, total):
    tick = yf.Ticker(company)
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
    get_info('SBER', 'D', 500)
    get_info('MOEX', 'D', 500)
    get_info('YNDX', 'D', 500)
    get_info('DSKY', 'D', 500)
    get_info('LKOH', 'D', 500)
    get_usa_company_info("META", 'D', 500)
    get_usa_company_info("AAPL", 'D', 500)

