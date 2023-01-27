import pandas as pd
import numpy as np
from main_settings import Path_Settings

ps = Path_Settings()


class Dataset():
    def __init__(self):
        self.df = pd.read_parquet(ps.path_dataset_processed_in_parquet)
        self.ttod_pdcd = self.total_order_demand_by('Product_Code')
        self.ttod_pdcat = self.total_order_demand_by('Product_Category')
        self.ttod_date = self.total_order_demand_by('Date')
        self.ttod_wh = self.total_order_demand_by('Warehouse')

        self.pv_dt_pdcd_od = self.pivot_productcode_date_orderdemand()


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

    def pivot_productcode_date_orderdemand(self):
        df = self.df
        grp = df.groupby(['Product_Code', 'Date'], as_index=False)['Order_Demand'].sum()
        pv = pd.pivot(grp, index='Date', columns='Product_Code', values='Order_Demand')
        pv.reset_index(inplace=True)
        pv.fillna(0, inplace=True)

        return pv
