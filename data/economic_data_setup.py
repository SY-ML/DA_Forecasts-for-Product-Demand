import pandas as pd
from dbnomics import fetch_series
from pandas_profiling import ProfileReport

from utils.reports import Reports

rpt = Reports()

dict_indexes = {'CCI': 'OECD', 'CPI': 'IMF'}

dict_CCI = {'China': 'OECD/DP_LIVE/CHN.CCI.AMPLITUD.LTRENDIDX.M',
            'UnitedStates': "OECD/DP_LIVE/USA.CCI.AMPLITUD.LTRENDIDX.M",
            'G20': 'OECD/DP_LIVE/G-20.CCI.AMPLITUD.LTRENDIDX.M',
            'OECDTotal': 'OECD/DP_LIVE/OECD.CCI.AMPLITUD.LTRENDIDX.M'}

dict_CPI = {'China': 'IMF/CPI/M.CN.PCPI_IX',
            'United_States' : 'IMF/CPI/M.US.PCPI_IX'}

class EconomicData_Setup():
    def __init__(self, save_to_path):
        self.path = save_to_path
        self.get_data_from('CCI', dict_CCI)
        self.get_data_from('CPI', dict_CPI)

    def get_data_from(self, index_name, dict):
        if index_name not in dict_indexes.keys():
            raise KeyError

        df = pd.DataFrame(fetch_series(dict))
        for key in dict:
            path = f'{self.path}/economic_indicators/{dict_indexes[index_name]}_{index_name}_{key}.csv'
            print(f"saving to {path}")
            df = pd.DataFrame(fetch_series(dict[key]))
            rpt.generate_profiling_report(df, path.replace('.csv', '.html'))
            df.to_csv(path, index=False)

