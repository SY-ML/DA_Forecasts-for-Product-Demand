import pandas as pd
from pandas_profiling import ProfileReport

class Reports():
    def __init__(self):
        pass

    def generate_profiling_report(self, df, save_as):
        profile = ProfileReport(df=df, explorative=True)
        profile.to_file(save_as)


