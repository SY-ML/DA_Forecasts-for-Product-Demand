from holidays import country_holidays
import pandas as pd

from main_settings import Path_Settings
ps = Path_Settings()



class Holidays():
    def __init__(self):
        self.df_CN = pd.read_csv(f'{ps.path_holidays_directory}/holiday_by_station_China(2012~2016).csv')
        self.df_US = pd.read_csv(f'{ps.path_holidays_directory}/holiday_by_station_UnitedStates(2012~2016).csv')


