import os
import pandas as pd
from utils.reports import Reports

rpt = Reports()

class CCI():
    def __init__(self, dataset_path):
        self.path = f"{dataset_path}/economic_indicators"
        self.CH, self.US, self.G20, self.OECD = self.all = self.load_CCI()

    def load_CCI(self):
        output = []
        for category in ['China', 'UnitedStates', 'G20', 'OECDTotal']:
            name_format = f'OECD_CCI_{category}.csv'
            path_file = f'../{self.path}/{name_format}'
            df = pd.read_csv(path_file)



            output.append(df)

        return output

#
#
# cci = CCI('archive')
#
# for df in cci.all:
#     print(df.shape)
#     print(df.columns)




