from holidays import country_holidays
import pandas as pd

from main_settings import Path_Settings
ps = Path_Settings()



class Holidays():
    def __init__(self):
        self.df_CN = pd.read_csv(f'{ps.path_holidays_directory}/holiday_by_station_China(2012~2016).csv', parse_dates= ['Date'])
        self.df_US = pd.read_csv(f'{ps.path_holidays_directory}/holiday_by_station_UnitedStates(2012~2016).csv', parse_dates= ['Date'])
        self.df_mgd = self.integrate_CN_and_US_holidays()
    def integrate_CN_and_US_holidays(self):
        df_CN, df_US = self.df_CN, self.df_US
        df_CN['country_code'] = 'CN'
        df_US['country_code'] = 'US'

        df_merged = pd.concat([df_CN, df_US], ignore_index=True)

        return df_merged



