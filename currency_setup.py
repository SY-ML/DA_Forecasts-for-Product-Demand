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
        self.load_and_save_data_with_code(code= code_cny_to_usd)


    def get_daily_data_with_code(self, code):
        data = yf.download(code, start = self.start_date, end = self.end_date, interval='1d')
        return data

    def load_and_save_data_with_code(self, code):
        data = self.get_daily_data_with_code(code)
        data.to_csv(f'{ps.path_currency_directory}/{ps.currency_nameformat}_{code}({self.start_date.year}-{self.end_date.year}).csv')


