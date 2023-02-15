import pandas as pd
from main_settings import Path_Settings

ps = Path_Settings()

class MeteoStats():
    def __init__(self):
        path_China = f'{ps.path_meteostat_directory}/{ps.meteostat_nameformat}_CN(2012~2016).csv'
        path_UnitedStates = f'{ps.path_meteostat_directory}/{ps.meteostat_nameformat}_US(2012~2016).csv'
        self.cn = self.read_and_process_csv_file(path_China, prefix='CN_')
        self.us = self.read_and_process_csv_file(path_UnitedStates, prefix='US_')

    def read_and_process_csv_file(self, path, prefix):

        df = pd.read_csv(path, parse_dates=['time'], on_bad_lines='skip', low_memory=False)
        '''
        #TODO-Handle the error
        The following issued was handled by setting on_bad_lines as skip
            pandas.errors.ParserError: Error tokenizing data. C error: Expected 14 fields in line 1829, saw 15
        '''

        # drop all columns except tavg because the other columns contain missing values
        df = df[['time', 'region', 'id', 'name', 'tavg']]

        # group by time and region
        grp = df.groupby(['region', 'time'])['tavg'].mean().reset_index()

        # pivot the data so that each region's average temperature in region columns
        pv = grp.pivot(index='time', columns='region', values='tavg')

        # add suffix
        pv = pv.add_prefix(prefix)
        pv = pv.add_suffix('(tavg)')
        pv.reset_index(inplace=True)

        return pv

