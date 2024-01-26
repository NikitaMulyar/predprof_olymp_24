from moexalgo import Ticker
import pandas as pd
from datetime import date, timedelta
from consts import moex_periods


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
    fromday = today - timedelta(minutes=minutes) - timedelta(minutes=60 * 24 * 95)  # Вычитаем квартал
    df = pd.DataFrame(tick.candles(date=fromday, till_date=today, period=moex_periods[period]))
    df = df[:total]
    df = df[['begin', 'open', 'close', 'high', 'low', 'value', 'volume', 'end']]
    # df.rename(columns={'volume': 'quantity'})
    df.to_csv(f'csv_files/{company}.csv')
