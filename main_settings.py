import os

class Path_Settings():
    def __init__(self):
        self.path_main = os.getcwd().replace('\\', '/')

        # dataset directory
        self.path_dataset_directory = './archive' # original dataset
        self.path_economic_indicators_directory = f'{self.path_dataset_directory}/economic_indicators' # economic indicators

        self.name_dataset = 'Historical Product Demand.csv' #original dadtaset name
        self.name_dataset_processed = 'Historical_Product_Demand_Processed.csv' # to-be dataset name after processing
        self.name_dataset_processed_parquet = 'Historical_Product_Demand_Processed.parquet' # to-be dataset name after converting to parquet

        self.path_dataset_original = f'{self.path_dataset_directory}/{self.name_dataset}'
        self.path_dataset_processed = f'{self.path_dataset_directory}/{self.name_dataset_processed}'
        self.path_dataset_processed_in_parquet = f'{self.path_dataset_directory}/{self.name_dataset_processed_parquet}'

        self.index_format_and_country_code = {'CCI': {'format': 'OECD_CCI',
                                                    'country_code': {'China': 'OECD/DP_LIVE/CHN.CCI.AMPLITUD.LTRENDIDX.M',
                                                                     'UnitedStates': "OECD/DP_LIVE/USA.CCI.AMPLITUD.LTRENDIDX.M",
                                                                     'G20': 'OECD/DP_LIVE/G-20.CCI.AMPLITUD.LTRENDIDX.M',
                                                                     'OECDTotal': 'OECD/DP_LIVE/OECD.CCI.AMPLITUD.LTRENDIDX.M'},
                                                      'path_merged': f'{self.path_economic_indicators_directory}/OECD_CCI_Merged.csv'
                                              },
                                      'CPI': {'format': 'IMF_CPI',
                                              'country_code':
                                                  {'China': 'IMF/CPI/M.CN.PCPI_IX',
                                                   'United_States': 'IMF/CPI/M.US.PCPI_IX'},
                                              'path_merged': f'{self.path_economic_indicators_directory}/IMF_CPI_Merged.csv'
                                              }
                                      }