import requests
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from main.data_storage.models import Company, StockSector

API_KEY = '4Z8JT1P9O38F9PY7'

class DataCenter:
    def __init__(self, symbol):
        self.symbol = symbol
        self.iex_base_url = "https://api.iextrading.com/1.0/"
        self.ts = TimeSeries(key=API_KEY, retries=100, output_format='pandas')
    def get_intraday(self, interval='15min', outputsize='compact'):
        return self.ts.get_intraday(symbol=self.symbol, interval=interval, outputsize=outputsize)
    def get_daily(self, outputsize='compact'):
        return self.ts.get_daily_adjusted(symbol=self.symbol, outputsize=outputsize)
    def get_weekly(self):
        return self.ts.get_weekly_adjusted(symbol=self.symbol)
    def get_monthly(self):
        return self.ts.get_monthly_adjusted(symbol=self.symbol)
    def get_latest(self):
        return self.ts.get_batch_stock_quotes(symbols=[self.symbol])
    def get_company(self):
        try:
            r = requests.get("{}stock/{}/company".format(self.iex_base_url, self.symbol))
            data = r.json()
            data = pd.DataFrame.from_dict(data, orient='columns').head(1)
            sector = StockSector.objects.get(name__icontains=str(data['sector'].values[0]))
            company = Company(name=data['companyName'].values[0], symbol=data['symbol'].values[0], description=data['description'].values[0], sector=sector)
            return company
        except Exception as err:
            return None