import pandas as pd
from main_settings import Path_Settings

ps = Path_Settings()

class MeteoStats():
    def __init__(self):
        path_china = f'{ps.path_meteostat_directory}/{ps.meteostat_nameformat}_CN(2012~2016).csv'
        self.cn = self.read_and_process_csv_file(path_china, prefix='CN_')

    def read_and_process_csv_file(self, path, prefix):
        df = pd.read_csv(path, parse_dates=['time'])

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
        # pv.rename(columns = {f'{prefix}time(tavg)':'time'}, inplace=True)

        return pv

