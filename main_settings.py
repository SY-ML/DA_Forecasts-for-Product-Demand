import os

class Path_Settings():
    def __init__(self):
        self.path_main = os.getcwd()
        self.path_dataset = './archive'
        self.path_economic_indicators = './archive/economic_indicators'

        self.name_dataset = 'Historical Product Demand.csv'
        self.name_dataset_processed = 'Historical_Product_Demand_Processed.csv'
        self.name_dataset_processed_parquet = 'Historical_Product_Demand_Processed.parquet'

        self.format_filename_CCI = 'OECD_CCI_'
        self.format_filename_CPI = 'IMF_CPI_'


