import os

import pandas as pd
from dbnomics import fetch_series
from pandas_profiling import ProfileReport

from utils.reports import Reports
from main_settings import Path_Settings

ps = Path_Settings()
rpt = Reports()

class Economic_Indicators_Setup():
    def __init__(self):
        self.make_direction()
        self.CCI = self.load_data_then_save('CCI')
        self.CPI = self.load_data_then_save('CPI')

    def make_direction(self):
        try:
            os.mkdir(ps.path_economic_indicators_directory)
        except:
            pass

    def load_data_then_save(self, index_name):
        dict_index = ps.index_format_and_country_code
        individual_index_data = dict_index[index_name] # data of each index
        # example) 'CCI' : {'format' : name format}, {country_code: { country : code}}}

        ls_index = dict_index.keys()

        # if an index not available is given, raise an error
        if index_name not in ls_index:
            raise KeyError

        # list of country_keys available
        ls_country = individual_index_data['country_code'].keys()

        # To-be path for economic indicator data
        indicator_directory = ps.path_economic_indicators_directory

        # For loop generating a csv file per country
        for i, country_key in enumerate(ls_country):
            # The chosen index's file name format
            file_name_format = individual_index_data['format']
            # add to-be directory and file name with the country name to the aforementioned format
            save_to_path = f'{indicator_directory}/{file_name_format}_{country_key}.csv'
            df = pd.DataFrame(fetch_series(individual_index_data['country_code'][country_key]))
            df.to_csv(save_to_path, index=False)
            print(f'Successfully saved! Path: {save_to_path}')

            # dataframe merge during the loop
            if i == 0:
                df_merge = df
            else:
                df_merge = pd.concat([df_merge, df])

        # The chosen index's file name format
        save_to_path_merged = individual_index_data['path_merged']
        # add to-be directory and file name 'Merged' to the aforementioned format
        # index_name_format = individual_index_data['format']
        # save_to_path_merged = f'{indicator_directory}/{index_name_format}_Merged.csv'
        df_merge.to_csv(save_to_path_merged, index= False)

        # convert the merged dataframe to a csv file

        # generate a pandas profiling report of the merged data frame
        rpt.generate_profiling_report(df_merge, save_as= save_to_path_merged.replace('.csv', '.html'))
        print(f'[{index_name}] Pandas profiling report successfully generated!')

