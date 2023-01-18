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

        self.get_ISO3166_2_subdivision_code(ISO3166_1_alpha_2_code= 'CN')
        # self.China_subdivs = pycountry.subdivisions.get(country_code=alpha2_China)
        # self.UnitedStates_subdivs = pycountry.subdivisions.get(country_code=alpha2_UnitedStates)

    def get_ISO3166_2_subdivision_code(self, ISO3166_1_alpha_2_code):
        data_set = list(pycountry.subdivisions.get(country_code= ISO3166_1_alpha_2_code))
        # data_set = pycountry.subdivisions.get(country_code= ISO3166_1_alpha_2_code)
        ls_subdivs = []
        for data_subdiv in data_set:
            ISO_3166_2_state = data_subdiv.code
            ls_subdivs.append(ISO_3166_2_state)
            stations = Stations().region(ISO3166_1_alpha_2_code, ISO_3166_2_state)
            print(stations.fetch(10, sample=True))


        # stations = Stations()

        return ls_subdivs

ctr = Countries()

print(ctr.get_ISO3166_2_subdivision_code('CN'))
print(ctr.get_ISO3166_2_subdivision_code('US'))
# print(a)
