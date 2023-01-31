import pandas as pd

def pandas_display_all(show_all=True):
    if show_all is True:
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
        else:
            pd.reset_option('all', None)
