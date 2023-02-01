import os
import pandas as pd
from main_settings import Path_Settings

ps = Path_Settings()


class Economic_Indicators():
    def __init__(self):

        self.cci = self.processed_CCI()
        self.cpi = self.processed_CPI()
        self.gdp = self.processed_GDP()

    def read_economic_indicator_data(self, index_name):
        path = ps.index_format_and_country_code[index_name]['path_merged']
        df = pd.read_csv(path)
        return df

    def processed_CCI(self):
        df = self.read_economic_indicator_data('CCI')
        df = df.pivot(index= 'original_period', columns = 'LOCATION', values= 'original_value')
        df = df.add_prefix('CCI_')
        df = df.reset_index()
        return df

    def processed_CPI(self):
        df = self.read_economic_indicator_data('CPI')
        df = df.pivot(index= 'original_period', columns= 'REF_AREA', values= 'original_value')
        df = df.add_prefix('CPI_')
        df = df.reset_index()
        return df

    def processed_GDP(self):
        df = self.read_economic_indicator_data('GDP')
        df = df.pivot(index='original_period', columns='LOCATION', values='original_value')
        # df = df.shift(periods=-1)
        # df.dropna(inplace=True)
        # df = df.add_prefix('PevYrGDP_')
        df = df.add_prefix('AnnGDP_')
        df = df.reset_index()
        return df