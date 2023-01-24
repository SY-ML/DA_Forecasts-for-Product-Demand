from holidays import country_holidays
import pandas as pd
from main_settings import Path_Settings
from utils.os_related import make_direction
ps = Path_Settings()

class Holidays_Setup():
    def __init__(self):
        make_direction(ps.path_holidays_directory)
        self.ls_years = [2012,2013,2014,2015,2016] # list of dataframe column names
        self.df_holidays_by_nation('China') # dataframe of Chinese holidays of the years
        self.df_holidays_by_nation('UnitedStates') # dataframe of American holidays of the years

    def df_holidays_by_nation(self, nation):
        data = country_holidays(country=nation, years = self.ls_years, observed=True)
        df = pd.DataFrame(data.items(), columns=['Date', 'Name'])
        df = df.sort_values(by='Date')
        df.to_csv(f'{ps.path_holidays_directory}/{ps.holidays_nameformat}_{nation}({min(self.ls_years)}~{max(self.ls_years)}).csv', index=False)

        return df

