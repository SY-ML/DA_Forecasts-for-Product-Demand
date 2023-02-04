from datetime import datetime

import meteostat
from meteostat import Point, Daily, Stations
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy import geocoders

import pycountry
import pandas as pd
'''
pip install pycountry
'''

from utils.os_related import make_direction
from main_settings import Path_Settings

import os

ps = Path_Settings()

class Meteostat_Setup():
    """
    # REF: List of ISO 3166 country codes
    https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
    """
    def __init__(self):
        make_direction(ps.path_meteostat_directory)
        country_code_in_alpha2_China = 'CN'
        country_code_in_alpha2_UnitedStates = 'US'
        # self.setup_meteostat_by_country(country_code_in_alpha2_China)
        self.setup_meteostat_by_country(country_code_in_alpha2_UnitedStates)


    def get_region_information_by_subdivision(self, ISO3166_1_alpha_2_code):
        data_set = pycountry.subdivisions.get(country_code= ISO3166_1_alpha_2_code)
        for i, data_subdiv in enumerate(data_set):
            ISO_3166_2_state = data_subdiv.code # subdivision code
            stations = Stations()
            country_code, state_code = ISO_3166_2_state.split('-')
            stations = stations.region(country_code, state_code)
            df_stations = stations.fetch()

            if i == 0: # In the first loop, copy the dataframe structure
                df_merge = df_stations
            else:
                df_merge = pd.concat([df_merge, df_stations])

        return df_merge

    def setup_meteostat_by_country(self, ISO3166_1_alpha_2_code):
        # get region information by country
        df_rgn = self.get_region_information_by_subdivision(ISO3166_1_alpha_2_code)

        # Specify date range
        year_from, year_to = 2012, 2016
        date_from, date_to = datetime(year_from, 1, 1), datetime(year_to, 12, 31)

        # Load data by station id
        for i, id in enumerate(df_rgn.index):
            data = Daily(id, start=date_from, end=date_to)
            df_daily = data.fetch().reset_index() #get data then reset as non-multi index
            df_daily['id'] = id
            df_daily['region'] = df_rgn.at[id, 'region']
            df_daily['name'] = df_rgn.at[id, 'name']
            path_csv = f'{ps.path_meteostat_directory}/{ps.meteostat_nameformat}_{ISO3166_1_alpha_2_code}({year_from}~{year_to}).csv'
            if i == 0: # in the first loop, get dataframe structure
                df_daily.to_csv(path_csv, index= False)
            else: # For the rest loops, concat
                df_daily.to_csv(path_csv, mode= 'a', header= False, index=False)
            print(f"PROCESSING {i}/{len(df_rgn)} ")

        # df_merge.to_csv(f'{ps.path_meteostat_directory}/{ps.meteostat_nameformat}_{ISO3166_1_alpha_2_code}({year_from}~{year_to}).csv', index= False)
