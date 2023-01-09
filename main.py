import datetime

import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib.style as style
style.use(['seaborn'])

""" Data Load """
df = pd.read_csv('./archive/Historical Product Demand.csv', parse_dates=['Date'])



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
df['Year'] = df['Date'].dt.year #연도
df['Month'] = df['Date'].dt.month # 월
df['Week'] = df['Date'].dt.isocalendar().week # 주 (week of the year)
df['DayOW'] = df['Date'].dt.dayofweek #요일 (day of the week) FYI) Mon 0 - Sun = 6
df['Year'] = df['Date'].dt.year.astype('Int16') #연도
df['Month'] = df['Date'].dt.month.astype('Int16') # 월
df['Week'] = df['Date'].dt.isocalendar().week # 주 (week of the year)
df['DayOW'] = df['Date'].dt.dayofweek.astype('Int16') #요일 (day of the week) FYI) Mon 0 - Sun = 6
df['Year_Month'] = df['Date'].dt.strftime('%Y-%m') # Time in %Y%m format
df['Year_Week'] = df['Date'].dt.strftime('%Y-%W') # Time in %Y%W format

print(df)

