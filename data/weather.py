from datetime import datetime
from meteostat import Point, Daily
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
        data_set = pycountry.subdivisions.get(country_code= ISO3166_1_alpha_2_code)

        for data_subdiv in data_set:
            a = data_subdiv.replace('Subdivision(', '')
            a = a.replace(')', '')
            a = a.split(',')
            print(a)
            # print(data_subdiv)

        # df = pd.DataFrame(data_set)
        # a = [subdiv for subdiv in data_set]
        print(data_set)
        # print(len(data_set))
        # a = [subdiv.split(',')[0] for subdiv in data_set]
        # print(a)
        # print(df)




c = Countries()

# print(c.China_subdivs)
# print(type(c.China_subdivs))
# print(c.UnitedStates_subdivs)


#
# class Weather_Data():
#     def __init__(self):
#         dict_cidites = {'China': ['Shanghai', 'Beijing', 'Guangzhou', 'Shenzhen', ],
#                         'UnitedStates' : []}
#
#         pass
#
#
#     def get_lat_and_long_with_city_name(self, city_name):
#         geolocator = Nominatim(user_agent='SY_ML')
#         loc = geolocator.geocode(city_name)
#         output = {'Location': loc, 'Latitude':loc.latitude, 'Longitude':loc.longitude}
#         return output
#
#
# wd = Weather_Data()
#
# # a = wd.get_lat_and_long_with_city_name('Shanghai')
# # a = wd.get_lat_and_long_with_city_name('Los Angeles')
# # a = wd.get_lat_and_long_with_city_name('Daegu')
# # print(a)
#
# g = geocoders.geonames('New York')
# a = g.address
# print(a)