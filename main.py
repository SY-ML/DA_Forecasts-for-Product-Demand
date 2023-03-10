import datetime
import numpy as np
import pandas as pd

import pandas_datareader as pdr
from pandas_datareader import yahoo
import pandas_datareader.data as web
import yfinance as yf

from tsfresh import extract_features, extract_relevant_features
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import  impute

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

from utils.pandas_related import pandas_display_all

from category_encoders import BinaryEncoder, OneHotEncoder

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

if __name__ == '__main__':

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
    df_gdp = ei.gdp
    # print(df_cci)
    # print(df_cpi)
    # print(df_gdp)

    hd = Holidays()

    # Chinese and American holidays
    df_hd = hd.calendar
    # print(df_hd)

    # cy = Currencies()
    # df_cny2usd_daily = cy.cny_to_usd_d
    # df_cny2usd_weekly = cy.cny_to_usd_w
    # df_cny2usd_monthly = cy.cny_to_usd_m

    ms = MeteoStats()
    df_meteo_CN = ms.cn
    df_meteo_US = ms.us
    # print(df_meteo_CN)
    # print(df_meteo_US)

    """
    Dataset preprocessing - merge
    """

    # merge with CCI on YYYY-MM
    df = df_pd.merge(df_cci, left_on='Year_Month', right_on='original_period', how='left')
    df.drop(columns='original_period', inplace=True) # drop duplicated data

    # merge with CPI on YYYY-MM
    df = df.merge(df_cpi, left_on='Year_Month', right_on='original_period', how='left')
    df.drop(columns='original_period', inplace=True) # drop duplicated data

    df = df.merge(df_gdp, left_on='Year', right_on='original_period', how='left')
    df.drop(columns='original_period', inplace=True) # drop duplicated data

    # merge with holidays on Date column
    df = df.merge(df_hd, how='left', on='Date')

    """ 
    HOLD: ????????? ??????????????? ????????? merge??? ?????? ??????
    # merge with CNY to USD rate
    # df = df.merge(df_cny2usd_daily, on='Date', how='left')
    df = df.merge(df_cny2usd_monthly, left_on='Year_Month', right_on='Date', how='left')
    """

    # merge with Chinese meteostats
    df = df.merge(df_meteo_CN, left_on='Date', right_on='time')
    df.drop(columns=['time'], inplace=True)
    # df = df.merge(df_meteo_US, left_on='Date', right_on='time')
    # df.drop(columns=['time'], inplace=True)

    print(df)
    print(df.columns)
    # exit()
    # print(df.isnull().sum())

    # Binary Encoding : categorical values
    be = BinaryEncoder(cols=['Product_Code', 'Warehouse', 'Product_Category', 'Year', 'Quarter', 'Month', 'Half', 'Week', 'DayOW'])
    df = be.fit_transform(df)
    print(df.columns)

    x = df.copy()[['Date', 'Holiday_CN', 'Holiday_US']]
    # x = df.copy().drop(columns='Order_Demand')
    y = df.copy()['Order_Demand']
    print(x, y)

    ### ToDo - filling unobserved rows


    # column_id added
    x['idx'] = x.index
    # features = extract_features(x, y, column_id='idx', column_sort='Date', pivot= False)
    features = extract_relevant_features(x, y, column_id='idx', column_sort='Date')
    print(features)

    ### ToDO - Data smoothing



    ### TODO - Data transformation : target encoding & normalization, standardization, or boxcox


    ### TODO - Build models
    # a. total demand forecasting
    # b. demand forecasting by warehouse
    # c. demand forecasting by product
    # d. anomaly prediction

##fadsf