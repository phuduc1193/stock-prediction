import requests
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

API_KEY = '4Z8JT1P9O38F9PY7'

class DataCenter:
    def __init__(self, symbol):
        self.symbol = symbol
        self.iex_base_url = "https://api.iextrading.com/1.0/"
        self.ts = TimeSeries(key=API_KEY, retries=100, output_format='pandas')

    def get_intraday(self, interval='15min', outputsize='compact'):
        df, meta_data = self.ts.get_intraday(symbol=self.symbol, interval=interval, outputsize=outputsize)
        return self.alter_data(df)

    def get_daily(self, outputsize='compact'):
        df, meta_data = self.ts.get_daily_adjusted(symbol=self.symbol, outputsize=outputsize)
        return self.alter_data(df)

    def get_weekly(self):
        df, meta_data = self.ts.get_weekly_adjusted(symbol=self.symbol)
        return self.alter_data(df)

    def get_monthly(self):
        df, meta_data = self.ts.get_monthly_adjusted(symbol=self.symbol)
        return self.alter_data(df)
        
    def get_company(self):
        try:
            r = requests.get("{}stock/{}/company".format(self.iex_base_url, self.symbol))
            data = r.json()
            data = pd.DataFrame.from_dict(data, orient='columns').head(1)
            return data
        except Exception as err:
            return None
    
    def alter_data(self, df):
        df.columns = ['Open', 'High', 'Low', 'Close', 'Adj. Close', 'Volume', 'Dividend', 'Split Coefficient']
        df['Date'] = pd.to_datetime(df.index.values)
        df['Volume'] = pd.to_numeric(df['Volume'], downcast='integer')
        df['Adj. Open'] = df['Open'] - df['Dividend']
        return df