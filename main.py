import datetime
import numpy as np
import pandas as pd

import pandas_datareader as pdr
from pandas_datareader import yahoo
import pandas_datareader.data as web
import yfinance as yf


import matplotlib.pyplot as plt
import seaborn as sns
from holidays import country_holidays

'''SY'''
from economic_data_setup import Economic_Indicators_Setup
from dataset_setup import Dataset_Setup
from meteostat_setup import Meteostat_Setup
from holidays_setup import Holidays_Setup
from currency_setup import Currency_Setup

from data.dataset import Dataset
from data.economic_data import Economic_Indicators
from data.holidays import Holidays
from data.currencies import Currencies
from data.meteostat import MeteoStats

from data_processor.converter import Converter

import matplotlib.style as style
style.use(['seaborn'])

def timeit(func):
    from functools import wraps
    import time
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


path_dataset_directory = './archive'
path = './archive/Historical Product Demand.csv' # path of the original dataset
path_prcd = './archive/Historical Product Demand(Processed).csv' #path of dataset to be processed
path_parquet = './archive/Historical_Product_Demand(Processed).parquet' # path of the dataset to be processed in a parquet format

# Generation of dataset with conversion and time feature additions in parquet format
# TODO-Inactivate after generation
# # Dataset SETUP
# Dataset_Setup() # Original dataset
# Economic_Indicators_Setup() # Economic indicators
# Meteostat_Setup()
# Holidays_Setup()
# Currency_Setup()
# cvt = Converter()

# dataframe to be used for the entire analysis
ds = Dataset()

# Product demand dataset
df_pd = ds.df
# print(df_pd)

ei = Economic_Indicators()

# CCI and CPI dataset
df_cci = ei.cci
df_cpi = ei.cpi
# print(df_cci)
# print(df_cpi)

hd = Holidays()
# Chinese and American holidays
df_hd = hd.calendar
# print(df_hd)

cy = Currencies()
df_cny2usd = cy.cny_to_usd
# print(df_cny2usd)

ms = MeteoStats()
df_meteo_CN = ms.cn
# print(df_meteo_CN)

"""
Dataset preprocessing - merge
"""

# merge with CCI on YYYY-MM
df = df_pd.merge(df_cci, left_on='Year_Month', right_on='original_period', how='left')
df.drop(columns='original_period', inplace=True) # drop duplicated data

# merge with CPI on YYYY-MM
df = df.merge(df_cpi, left_on='Year_Month', right_on='original_period', how='left')
df.drop(columns='original_period', inplace=True) # drop duplicated data

# merge with holidays on Date column
df = df.merge(df_hd, how='left', on='Date')

# merge with CNY to USD rate
df = df.merge(df_cny2usd, on='Date', how='left')

data = yf.download('CNY=X', start = '2021-01-01', end = '2022-12-31', interval='1wk')
# todo - 화폐 주단위로 바꿔주기

print(data)
# print(df_cny2usd.isnull().sum())
# print(df.isnull().sum())
# print(df[df['Open(CNY=X)'].isnull()][['Date', 'Open(CNY=X)']])
# print(df_cny2usd.columns)
# print(df_cny2usd)
# merge with Chinese average temperature by region
# df = df.merge()
# print(df)
# print(df.columns)


exit()
#
sns.heatmap(df_prcd.corr(), cmap='RdBu', vmin=-1, vmax=1, annot=True, fmt='.2f')
plt.show()
