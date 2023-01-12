from holidays import country_holidays
import pandas as pd

class Holidays():
    def __init__(self, ls_years):
        self.ls_years = ls_years # list of dataframe column names
        self.df_ch_hol = self.df_holidays_by_nation('China') # dataframe of Chinese holidays of the years
        self.df_us_hol = self.df_holidays_by_nation('UnitedStates') # dataframe of American holidays of the years

    def df_holidays_by_nation(self, nation):
        data = country_holidays(country=nation, years = self.ls_years, observed=True)
        df = pd.DataFrame(data.items(), columns=['Date', 'Name'])
        df = df.sort_values(by='Date')

        return df