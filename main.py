import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from holidays import country_holidays

'''SY'''
from data.dataset_setup import Dataset_Setup
from data.dataset import Dataset
from data.holidays import Holidays

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

def display_all_on():
 pd.set_option('display.max_rows', None)
 pd.set_option('display.max_columns', None)


def display_all_off():
 pd.reset_option('all', None)

path = './archive/Historical Product Demand.csv' # path of the original dataset
path_prcd = './archive/Historical Product Demand(Processed).csv' #path of dataset to be processed
path_parquet = './archive/Historical_Product_Demand(Processed).parquet' # path of the dataset to be processed in a parquet format

# Generation of dataset with conversion and time feature additions in parquet format
# TODO-Inactivate after generation
# Dataset_Setup(path_orgcsv=path, path_prcdcsv= path_prcd, path_prcdpq= path_parquet)

# dataframe to be used for the entire analysis
ds = Dataset(path_pq= path_parquet)

df = ds.df.copy()
ls_years = df['Year'].unique()
ch = Holidays(ls_years= ls_years)
# display_all_on()
print(ch.df_ch_hol)
print(ch.df_us_hol)


# print(df.groupby('Date').count())
#
# for year in [2011, 2012, 2013, 2014, 2015, 2016, 2017]:
#     data = df[df['Year'] == year]['Date'].unique()
#     print(f'{year} - {len(data)}')