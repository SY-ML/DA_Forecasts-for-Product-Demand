import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from holidays import country_holidays

'''SY'''
from economic_data_setup import Economic_Indicators_Setup
from dataset_setup import Dataset_Setup
from meteostat_setup import Meteostat_Setup
from holidays_setup import Holidays_Setup

from data.dataset import Dataset
from data.economic_data import Economic_Indicators
from data.holidays import Holidays

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

# cvt = Converter()

# dataframe to be used for the entire analysis
ds = Dataset()
# print(ds.df)
ei = Economic_Indicators()
# print(ei.cci)
# print(ei.cpi)
hd = Holidays()
# print(hd.calendar)

"""
Dataset preprocessing - merge
"""
df = ds.df
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d') # string-type date data conversion to datetime type

# merge with CCI on YYYY-MM
df = df.merge(ei.cci, left_on='Year_Month', right_on='original_period', how='left', suffixes=(None, 'CCI_'))
df.drop(columns='original_period', inplace=True) # drop duplicated data
df.rename(columns={'CHN':'CCI_CN', 'G-20': 'CCI_G20', 'OECD': 'CCI_OECD', 'USA':'CCI_US'}, inplace=True)

# merge with CPI on YYYY-MM
df = df.merge(ei.cpi, left_on='Year_Month', right_on='original_period', how='left')
df.drop(columns='original_period', inplace=True) # drop duplicated data
df.rename(columns={'CN':'CPI_CN', 'US':'CPI_US'}, inplace=True)

# merge with holidays on Date column
df_prcd = df.merge(hd.calendar, how='left', on='Date')
print(df_prcd)
print(df_prcd.columns)

sns.heatmap(df_prcd.corr(), cmap='RdBu', vmin=-1, vmax=1, annot=True, fmt='.2f')
plt.show()
print(df_prcd.corr())
exit()
# print(df_prcd['Date'].dtype)
# print(df_prcd['Date'])
# print(hd.calendar['Date'].dtype)
