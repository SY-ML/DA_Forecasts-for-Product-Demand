from holidays import country_holidays
import pandas as pd

from main_settings import Path_Settings
from main_settings import TUPLE_DATEFROM_AND_DATETO
ps = Path_Settings()



class Holidays():
    def __init__(self):
        self.df_CN = pd.read_csv(f'{ps.path_holidays_directory}/holiday_by_station_China(2012~2016).csv', parse_dates= ['Date'])
        self.df_US = pd.read_csv(f'{ps.path_holidays_directory}/holiday_by_station_UnitedStates(2012~2016).csv', parse_dates= ['Date'])
        self.calendar = self.load_data_range_with_holiday_marked()

    def integrate_CN_and_US_holidays(self):
        df_CN, df_US = self.df_CN, self.df_US
        df_CN['Holiday'] = 'CN'
        df_US['Holiday'] = 'US'

        df_merged = pd.concat([df_CN, df_US], ignore_index=True)

        return df_merged
    
    def load_data_range_with_holiday_marked(self):
        
        df_mgd = self.integrate_CN_and_US_holidays()
        df_mgd = pd.get_dummies(df_mgd, columns=['Holiday'])
        
        date_from, date_to = TUPLE_DATEFROM_AND_DATETO()
        
        date_range = pd.DataFrame(
            {'Date': pd.date_range(date_from, date_to)})

        calendar = date_range.merge(df_mgd, how='left', on='Date')
        calendar.drop(columns=['Name'], inplace=True)
        calendar.fillna(0, inplace=True)
        
        return calendar


