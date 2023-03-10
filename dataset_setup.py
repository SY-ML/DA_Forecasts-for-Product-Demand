import pandas as pd
import pyarrow.csv as pv
import pyarrow.parquet as pq
import numpy as np

from main_settings import Path_Settings

ps = Path_Settings()

class Dataset_Setup():
    def __init__(self):
        self.path = ps.path_dataset_original
        self.path_prcd = ps.path_dataset_processed
        self.path_parquet = ps.path_dataset_processed_in_parquet

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
        df['Year_Week'] = df['Date'].dt.year.astype(str)+'-'+df['Date'].dt.isocalendar().week.astype(str)  # Time in %Y%m format

        # Save data generated between 2012 and 2016 only
        df = df.loc[(df['Year']>=2012)&(df['Year']<=2016)]

        df.to_csv(self.path_prcd, index=False)

    def convert_processed_dataframe_from_csv_to_parquet(self):
        """
        Writes the processed dataset in a parquet format after reading the processed dataset in csv format
        :return:None
        """
        df = pv.read_csv(self.path_prcd)
        pq.write_table(df, self.path_parquet)

