import pandas as pd
from main_settings import Path_Settings

ps = Path_Settings()

class Currencies():
    def __init__(self):
        code_cny_to_usd = 'CNY=X'
        self.cny_to_usd_d = self.read_and_precoess_csv_file(code_cny_to_usd, basis = 'daily')
        self.cny_to_usd_w = self.read_and_precoess_csv_file(code_cny_to_usd, basis = 'weekly')
        self.cny_to_usd_m = self.read_and_precoess_csv_file(code_cny_to_usd, basis = 'monthly')

    def read_and_precoess_csv_file(self, code, basis):
        valid_basis = ['daily', 'weekly', 'monthly']
        path = f'{ps.path_currency_directory}/{ps.currency_nameformat}_{basis}_{code}(2012-2016).csv'
        df = pd.read_csv(path)

        # add features : Range = Max - Min
        df['H-L_Range'] = df['High'] - df['Low']
        df['O-C_Range'] = df['Open'] - df['Close']

        # string-type data in '%Y-%m-%d %H:%M:%S%z' format to datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S%z', utc=True).dt.tz_localize(None)

        if basis not in valid_basis:
            raise KeyError

        if basis == 'weekly':
            df['Date'] = df['Date'].dt.year.astype(str)+'-'+df['Date'].dt.isocalendar().week.astype(str)
            # df['Date'] = df['Date'].dt.strftime('%Y-%W')
        elif basis == 'monthly':
            df['Date'] = df['Date'].dt.strftime('%Y-%m')



        # drop adj_close, volume column
        df.drop(columns=['Adj Close', 'Volume'], inplace=True)

        # add prefix
        df = df.add_suffix(f'({code})')
        df.rename(columns={f'Date({code})': 'Date'}, inplace=True)

        return df
