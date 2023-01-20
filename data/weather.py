from datetime import datetime
from meteostat import Point, Daily, Stations
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy import geocoders

import pycountry
import pandas as pd
'''
pip install pycountry
'''

class Countries():
    """
    # REF: List of ISO 3166 country codes
    https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
    """
    def __init__(self):
        alpha2_China = 'CN'
        alpha2_UnitedStates = 'US'
        self.rgn_CN = self.get_region_information_by_subdivision(alpha2_China)
        self.rgn_US = self.get_region_information_by_subdivision(alpha2_UnitedStates)

    def get_region_information_by_subdivision(self, ISO3166_1_alpha_2_code):
        data_set = pycountry.subdivisions.get(country_code= ISO3166_1_alpha_2_code)
        for i, data_subdiv in enumerate(data_set):
            ISO_3166_2_state = data_subdiv.code # subdivision code
            stations = Stations()
            country_code, state_code = ISO_3166_2_state.split('-')
            stations = stations.region(country_code, state_code)
            df_stations = stations.fetch()

            if i == 0:
                df_merge = pd.DataFrame(columns=df_stations.columns)
            else:
                df_merge = pd.concat([df_merge, df_stations])
        # stations = Stations()

        return df_merge

    def get_weather_data_by_subdivision(self, ISO3166_1_alpha_2_code):
    # def get_weather_data_by_subdivision(self, ISO3166_1_alpha_2_code, date_from, date_to):
        df_rgn = self.get_region_information_by_subdivision(ISO3166_1_alpha_2_code)
        date_from = datetime(2022, 1, 20)
        date_to = datetime(2022, 3, 30)
        data = Daily('10637', start=date_from, end=date_to).fetch()
        print(data)


ctr = Countries()

# print(ctr.rgn_US.columns)
# print(ctr.rgn_US)
print(ctr.get_weather_data_by_subdivision('CN'))