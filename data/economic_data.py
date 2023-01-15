import os
import pandas as pd
from utils.reports import Reports

rpt = Reports()

class CCI():
    def __init__(self, dataset_path):
        self.path = f"{dataset_path}/economic_indicators"
        # self.CH, self.US, self.G20, self.OECD = self.all = self.load_CCI()
        self.df = self.merge_CCI_data(report=False)
        self.df_prcd = self.process_merged_CCI_data()

    def load_CCI(self):
        output = []

        for category in ['China', 'UnitedStates', 'G20', 'OECDTotal']:
            name_format = f'OECD_CCI_{category}.csv'
            path_file = f'../{self.path}/{name_format}'
            df = pd.read_csv(path_file)
            output.append(df)

        return output

    def merge_CCI_data(self, report=False):
        df_concat = pd.DataFrame(columns=self.load_CCI()[0].columns)

        for df in self.load_CCI():
            df_concat = pd.concat([df_concat, df])

        # path_report = f'{self.path}/OECD_CCI_Merged.html'
        # print(f"path_report = {path_report}")
        # rpt.generate_profiling_report(df = df_concat, save_as=path_report)

        return df_concat

    def process_merged_CCI_data(self):
        df = self.df

        df = df[['period', 'original_value', 'value', 'Country', 'Indicator']]

        return df
#
#
cci = CCI('archive')
import os
a = os.getcwd()
print(a)
exit()
from utils.pandas_display import Display_Option
# Display_Option(show_all=True)
df = cci.df_prcd
# print(cci.df.head())
print(cci.df.columns)
print(df)
# print(df['SUBJECT'].value_counts())
# print(df.head())
# print(df['series_code'].value_counts())

#
# print(cci.df.columns)
#
# for df in cci.all:
#     print(df.shape)
#     print(df.columns)




