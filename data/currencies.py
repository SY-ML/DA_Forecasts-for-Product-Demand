import pandas as pd
from main_settings import Path_Settings

ps = Path_Settings()

class Currencies():
    def __init__(self):
        path_cny_to_usd = f'{ps.path_currency_directory}/{ps.currency_nameformat}_CNY=X(2012-2016).csv'
        self.cny_to_usd = pd.read_csv(path_cny_to_usd)
