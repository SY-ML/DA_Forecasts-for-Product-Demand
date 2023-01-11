import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyarrow.csv as pv
import pyarrow.parquet as pq

''' pip install Chinese-holiday '''
import chinese_holiday as ch

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

class Dataset_Setup():
    def __init__(self, path_orgcsv, path_prcdcsv, path_prcdpq):
        self.path = path_orgcsv # path of the original dataset
        self.path_prcd = path_prcdcsv #path of dataset to be processed
        self.path_parquet = path_prcdpq # path of the dataset to be processed in a parquet format

        self.df_org = pd.read_csv(self.path, parse_dates=['Date']) # original dataset read
        self.df = self.df_org.loc[self.df_org['Warehouse'] != 'Whse_A'].reset_index(drop = True) # dataset with added time features

        self.generate_dataset_processed() #
        self.convert_processed_dataframe_from_csv_to_parquet()

    def generate_dataset_processed(self):
        """
        Save the processed dataset after converting string to integer and adding time features extracted from 'Date' column
        :return: None
        """
        df = self.df
        """ Data Conversion """
        # Product_Code
        df['Product_Code'] = df['Product_Code'].str.replace('Product_', '').astype(int)
        # Warehouse
        df['Warehouse'] = df['Warehouse'].str.replace('Whse_', '')
        # Product_Category
        df['Product_Category'] = df['Product_Category'].str.replace('Category_', '').astype(int)

        # Order Demand
        df['Order_Demand'] = df['Order_Demand'].replace('[)]', '', regex=True)
        df['Order_Demand'] = df['Order_Demand'].replace('[(]', '-', regex=True)
        df['Order_Demand'] = df['Order_Demand'].astype(int)

        # Basic Time Features
        df['Year'] = df['Date'].dt.year  # 연도
        df['Quarter'] = df['Date'].dt.quarter  # 월
        df['Month'] = df['Date'].dt.month  # 월
        df['Half'] = np.where(df['Month'] <= 6, 1, 2)
        df['Week'] = df['Date'].dt.isocalendar().week  # 주 (week of the year)
        df['DayOW'] = df['Date'].dt.dayofweek  # 요일 (day of the week) FYI) Mon 0 - Sun = 6
        df['Year'] = df['Date'].dt.year.astype('Int16')  # 연도
        df['Month'] = df['Date'].dt.month.astype('Int16')  # 월
        df['DayOW'] = df['Date'].dt.dayofweek.astype('Int16')  # 요일 (day of the week) FYI) Mon 0 - Sun = 6
        df['Year_Month'] = df['Date'].dt.strftime('%Y-%m')  # Time in %Y%m format
        df['Year_Week'] = df['Date'].dt.strftime('%Y-%W')  # Time in %Y%W format

        # df['Holiday'] = np.where(df[df['Date']])

        df.to_csv(self.path_prcd, index=False)

    def convert_processed_dataframe_from_csv_to_parquet(self):
        """
        Writes the processed dataset in a parquet format after reading the processed dataset in csv format
        :return:None
        """
        df = pv.read_csv(self.path_prcd)
        pq.write_table(df, self.path_parquet)




class Dataset():
    def __init__(self, path_pq):
        self.df = pd.read_parquet(path_pq)
        self.ttod_pdcd = self.total_order_demand_by('Product_Code')
        self.ttod_pdcat = self.total_order_demand_by('Product_Category')
        self.ttod_date = self.total_order_demand_by('Date')
        self.ttod_wh = self.total_order_demand_by('Warehouse')

    def total_order_demand_by(self, col):
        return self.df.groupby(col, as_index=False)['Order_Demand'].sum()

    def order_correction_data_by_date_and_product_code(self):
        df = self.df.copy()
        df['OD_Pos'] = np.where(df['Order_Demand'] > 0, df['Order_Demand'], 0)
        df['OD_Neg'] = np.where(df['Order_Demand'] < 0, df['Order_Demand'], 0)

        grp = df.groupby(['Date', 'Product_Code'], as_index=False).agg(OD_Pos_sum=('OD_Pos', 'sum'),
                                                                 OD_Pos_count=('OD_Pos', 'count'),
                                                                 OD_Neg_sum=('OD_Neg', 'sum'),
                                                                 OD_Neg_count=('OD_Neg', 'count'),
                                                                 OD_Total_sum=('Order_Demand', 'sum'),
                                                                 OD_Total_count=('Order_Demand', 'count'))

        return grp



    # def correction_times_and_amount_per_day(self):


path = './archive/Historical Product Demand.csv' # path of the original dataset
path_prcd = './archive/Historical Product Demand(Processed).csv' #path of dataset to be processed
path_parquet = './archive/Historical_Product_Demand(Processed).parquet' # path of the dataset to be processed in a parquet format

# Generation of dataset with conversion and time feature additions in parquet format
# TODO-Inactivate after generation
# Dataset_Setup(path_orgcsv=path, path_prcdcsv= path_prcd, path_prcdpq= path_parquet)

# dataframe to be used for the entire analysis
ds = Dataset(path_pq= path_parquet)

# print(ds.ttod_pdcd)
# print(ds.ttod_pdcat)
# print(ds.ttod_date)
# print(ds.ttod_wh)
#
# df = ds.df.copy()
# df['OD_Pos'] = np.where(df['Order_Demand']>0, df['Order_Demand'], 0)
# df['OD_Neg'] = np.where(df['Order_Demand']<0, df['Order_Demand'], 0)
#
# grp = df.groupby(['Date', 'Product_Code'], as_index=False)
#
#
# df.groupby(['Date', 'Product_Code'], as_index=False).agg(OD_Pos_sum = ('OD_Pos', 'sum'), OD_Pos_count = ('OD_Pos', 'count'),
#                                                              OD_Neg_sum = ('OD_Neg', 'sum'), OD_Neg_count = ('OD_Neg', 'count'),
#                                                              OD_Total_sum = ('Order_Demand', 'sum'), OD_Total_count = ('Order_Demand', 'count'))
#
#

# print(ds.order_correction_data_by_date_and_product_code())


# print(ds.df.head(1)['Date'])

df = ds.df.copy()
df['Date'] = df['Date'].astype(str)
# df['Date'] = ch.is_holiday(df['Date'].astype(str))
# print(df['Date'])
print(df['Date'].dtype)