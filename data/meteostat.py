import pandas as pd
from main_settings import Path_Settings


class MeteoStats():
    def __init__(self):
        self.cn = pd.read_csv(f'{ps.path_meteostat_directory}/{ps.meteostat_nameformat}_CN(2012~2016).csv')