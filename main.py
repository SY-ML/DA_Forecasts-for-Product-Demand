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
from data.economic_data_setup import EconomicData_Setup
from data.economic_data import CCI

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


path_dataset = './archive'
path = './archive/Historical Product Demand.csv' # path of the original dataset
path_prcd = './archive/Historical Product Demand(Processed).csv' #path of dataset to be processed
path_parquet = './archive/Historical_Product_Demand(Processed).parquet' # path of the dataset to be processed in a parquet format

# Generation of dataset with conversion and time feature additions in parquet format
# TODO-Inactivate after generation
# # Dataset Setup
# Dataset_Setup(path_orgcsv=path, path_prcdcsv= path_prcd, path_prcdpq= path_parquet)
# # Economic Indicator Setup
# EconomicData_Setup(save_to_path = path_dataset)

# dataframe to be used for the entire analysis
ds = Dataset(path_pq= path_parquet)
cvt = Converter()

df = ds.df.copy()

# cci = CCI(dataset_path=path_dataset)
# print(cci.US)


# ls_years = df['Year'].unique()
# df_hol = Holidays(ls_years= ls_years)
# dict_holiday = {'US': df_hol.df_us_hol['Date'].tolist(), 'CH': df_hol.df_ch_hol['Date'].tolist()}
# df_ODByDate = ds.ttod_date.copy()
# for nation in dict_holiday.keys():
#     col_name = f'Holiday_{nation}'
#     df_ODByDate[col_name] = df_ODByDate['Date'].apply(lambda x: x in dict_holiday[nation])
#     df_ODByDate[col_name] = cvt.convert_bool_to_int(df_ODByDate[col_name])

