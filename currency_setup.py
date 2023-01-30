import yfinance as yf
import pandas as pd
from utils.os_related import make_direction
from main_settings import Path_Settings, TUPLE_DATEFROM_AND_DATETO

ps = Path_Settings()

class Currency_Setup():
    def __init__(self):
        make_direction(ps.path_currency_directory)
        code_cny_to_usd = 'CNY=X'
        self.start_date, self.end_date = TUPLE_DATEFROM_AND_DATETO()
        self.load_and_save_data_with_code(code= code_cny_to_usd, basis = 'daily')
        self.load_and_save_data_with_code(code= code_cny_to_usd, basis = 'weekly')
        self.load_and_save_data_with_code(code= code_cny_to_usd, basis = 'monthly')


    def get_daily_data_with_code(self, code):
        data = yf.download(code, start = self.start_date, end = self.end_date, interval='1d')
        return data

    def get_weekly_data_with_code(self, code):
        data = yf.download(code, start = self.start_date, end = self.end_date, interval='1wk')
        return data

    def get_monthly_data_with_code(self, code):
        data = yf.download(code, start = self.start_date, end = self.end_date, interval='1mo')
        return data


    def load_and_save_data_with_code(self, code, basis):
        if basis == 'daily':
            data = self.get_daily_data_with_code(code)
        elif basis == 'weekly':
            data = self.get_weekly_data_with_code(code)
        elif basis == 'monthly':
            data = self.get_monthly_data_with_code(code)
        else:
            raise KeyError

        data.reset_index(inplace=True)
        data.to_csv(f'{ps.path_currency_directory}/{ps.currency_nameformat}_{basis}_{code}({self.start_date.year}-{self.end_date.year}).csv', index=False)



