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
Meteostat_Setup()
# Holidays_Setup()

# cvt = Converter()

# dataframe to be used for the entire analysis
# ds = Dataset()
# print(ds.df)
# ei = Economic_Indicators()
# print(ei.cci)
# print(ei.cpi)
# hd = Holidays()
# print(hd.df_CN)
# print(hd.df_US)