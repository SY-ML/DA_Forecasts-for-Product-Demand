'''
https://www.kaggle.com/datasets/felixzhao/productdemandforecasting/code
'''
import datetime

import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib.style as style
"""
print(plt.style.available)
['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark', 'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10']

"""
style.use(['seaborn'])

df = pd.read_csv('./archive/Historical Product Demand.csv', parse_dates=['Date'])
# df = pd.read_csv('./archive/Historical Product Demand.csv')
# print(df.dtypes)
# print(df.columns)
"""
EDA Report
"""
# profile = ProfileReport(df= df, explorative=True)
# profile.to_file('pd_profile.html')


"""
Data Conversion
"""
# Product_Code
df['Product_Code'] = df['Product_Code'].str.replace('Product_', '').astype(int)
# Warehouse
df['Warehouse'] = df['Warehouse'].str.replace('Whse_', '')

# Product_Category
df['Product_Category'] = df['Product_Category'].str.replace('Category_', '').astype(int)

# Date
# df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d').dt.date.replace({pd.NaT:np.nan})

# Order Demand
df['Order_Demand'] = df['Order_Demand'].replace('[)]', '', regex=True)
df['Order_Demand'] = df['Order_Demand'].replace('[(]', '-', regex=True)
df['Order_Demand'] = df['Order_Demand'].astype(int)

# print(df.dtypes)
# print(df.columns)

'''
Time Data 
'''
df['Year'] = df['Date'].dt.year #연도
df['Month'] = df['Date'].dt.month # 월
df['Week'] = df['Date'].dt.isocalendar().week # 주 (week of the year)
df['DayOW'] = df['Date'].dt.dayofweek #요일 (day of the week) FYI) Mon 0 - Sun = 6
df['Year'] = df['Date'].dt.year.astype('Int16') #연도
df['Month'] = df['Date'].dt.month.astype('Int16') # 월
df['Week'] = df['Date'].dt.isocalendar().week # 주 (week of the year)
df['DayOW'] = df['Date'].dt.dayofweek.astype('Int16') #요일 (day of the week) FYI) Mon 0 - Sun = 6

# print(df[['Date', 'Year', 'Month', 'Week', 'DayOW']])

"""
Data Exploration
"""
print(df.columns)


## 제품별 전체수요
# grp_byPC = df.groupby('Product_Code', as_index=False)['Order_Demand'].sum() #제품 수요 합계
# grp_byPC = pd.DataFrame(grp_byPC).sort_values(by = 'Order_Demand', ascending=False, ignore_index=True) #데이터프레임 변화 후 Order_Demand에 따라 내림차순 정렬
# grp_byPC['Demand_Proportion'] = (grp_byPC['Order_Demand']/grp_byPC['Order_Demand'].sum()) #전체 판매량의 기여도를 pct로 변환
# grp_byPC['Demand_Accumulated'] = grp_byPC['Demand_Proportion'].cumsum() #기여도 누적합계
# grp_byPC['Demand_80pct'] = 0
# grp_byPC.loc[grp_byPC['Demand_Accumulated'] <= 0.8, 'Demand_80pct'] = 1 #Demand 기여도 80%에 든다면 1로 표기

# print(grp_byPC)
# print(grp_byPC[grp_byPC['Demand_80pct'] == 1]['Product_Code'].unique())
# print(grp_byPC[grp_byPC['Demand_80pct'] == 1]['Product_Code'].nunique())
# print(grp_byPC['Product_Code'].nunique())
# print(grp_byPC[grp_byPC['Demand_80pct'] == 1]['Product_Code'].nunique() / grp_byPC['Product_Code'].nunique())

# ls_pcin80 = grp_byPC[grp_byPC['Demand_80pct'] == 1]['Product_Code'].unique() # Demand 상위 80%내 제품의 제품코드


## 카테고리 별
# grp_byPCAT = df.groupby('Product_Category', as_index=False)['Order_Demand'].sum() #제품 수요 합계
# grp_byPCAT = pd.DataFrame(grp_byPCAT).sort_values(by = 'Order_Demand', ascending=False, ignore_index=True) #데이터프레임 변화 후 Order_Demand에 따라 내림차순 정렬
#
# print(grp_byPCAT['Product_Category'].nunique()) # 전체 제품 카테고리 수
# plt.pie(grp_byPCAT['Order_Demand'], labels = grp_byPCAT['Product_Category'], autopct='%.1f')
# plt.title('Proportion of Order Demand By Product_Category')
# plt.legend(loc='best')
# plt.show()
#
# ls_pcat_top4 = [19, 6, 5, 7] #Demand 상위 97%의 제품 카테고리 번호

# 웨어하우스 별
# grp_byWH = df.groupby('Warehouse', as_index=False).agg({'Product_Code':['nunique'],
#                                                         'Product_Category':['nunique'],
#                                                         'Order_Demand':['sum', 'min', 'max', 'mean', 'median', 'std']})

# GROUP BY
# print(grp_byWH.T)

# Order Demand By Warehouse Boxplot
# sns.boxplot(data = df, x='Warehouse', y='Order_Demand')
# plt.title('ORDER DEMAND BOXPLOT BY WAREHOUSE')
# plt.show()

## Order Demand
# unique, counts = np.unique(df['Order_Demand'], return_counts=True)
# sns.histplot(x=unique, y=counts, kde=True)
# sns.kdeplot(df['Order_Demand'])

# Positive/Negative Order Demand
# df_od = df.copy()
# df_od['OD_Positive'] = np.where(df_od['Order_Demand']>=0, 1, 0)

# KDE PLOT
# sns.kdeplot(df_od['Order_Demand'])
# plt.title('DISTRIBUTION OF ORDER DEMAND')
# plt.show()

# PIE PLOT
# plt.pie(df_od['OD_Positive'].value_counts(), labels = df_od['OD_Positive'].value_counts().index, autopct='%.1f')
# plt.title('ORDER DEMAND POSITIVE/NEGATIVE')
# plt.legend(loc='best')
# plt.show()
# print(df_od['OD_Positive'].value_counts())


# f, ax = plt.subplots(1, 2)
# sns.violinplot(data = df_od, x='Warehouse', y='Order_Demand', ax=ax[0])
# ax[0].set_title('Order Demand Distribution By Warehouse')
# sns.violinplot(data = df_od, x='Warehouse', y='Order_Demand', hue='OD_Positive', scale='count', split=True, ax=ax[1])
# ax[1].set_title('Order Demand Distribution By Warehouse (Positive/Negative)')
# f.suptitle('DISTRIBUTION OF ORDER DEMAND BY WAREHOUSE')
# plt.show()


# Negative order demand가 있었던 창고/날짜 조사
# df_negOD = df_od[(df['Order_Demand']<0) & (df['Date'].notnull())] # Filter (negative order demand & not-null date data)
# grp_negOD = df_negOD.groupby(['Date', 'Warehouse'], as_index=False )['Product_Code'].nunique() #Date, WH 기준으로 그룹화 후 날짜/창고별 음수 order demand
# grp_negOD_sample = grp_negOD.sort_values(by=['Product_Code'], ascending=False).head() # Product 기준으로 정렬 후 상위 5개 데이터만 선택
# negOD_info = zip(grp_negOD_sample['Date'], grp_negOD_sample['Warehouse']) # Date, WH 코드를 결합

def display_all_on():
 pd.set_option('display.max_rows', None)
 pd.set_option('display.max_columns', None)


def display_all_off():
 pd.reset_option('all', None)


# display_all_on()
## for info in negOD_info:
#  print(f"DATA: {info}")
#  view = df[(df['Date'] == info[0]) & (df['Warehouse'] == info[1])] # data for view based on the info
#  print(view[['Date', 'Warehouse', 'Product_Code', 'Order_Demand']].sort_values(by=['Product_Code']))
#  print('-')

# # Sum > Negative case
# grp_OD_sum = df.groupby(['Date', 'Product_Code', 'Warehouse'], as_index=False)['Order_Demand'].sum()
# grp_OD_negSum = grp_OD_sum[grp_OD_sum['Order_Demand']<0]
# print(grp_OD_negSum)

# # 2011년 10월 웨어하우스 S에서 Produdct 125 오더 디맨드
# print(df[(df['Date']>datetime.date(2011,10,1)) & (df['Date']<datetime.date(2011,10,30))& (df['Warehouse'] == 'S') & (df['Product_Code'] == 125)])

"""
EDA with Time Series
"""
# Additional Time features
df['Year_Month'] = df['Date'].dt.strftime('%Y-%m')
df['Year_Week'] = df['Date'].dt.strftime('%Y-%W')


# Order Demand by year and date
cols_view = ['Year', 'Year_Month', 'Year_Week', 'Date']

# # Data Distribution Check
# print(df.groupby('Year')['Order_Demand'].count())
# print(df['Date'].min(), df['Date'].max())
#
# for col in cols_view:
#  df_view = df.copy().sort_values(by=col)
#  # sns.barplot(data=data, kde=True)
#  sns.histplot(data=df_view, x=col, kde=True)
#  # sns.histplot(data=df, x=col, kde=True)
#  plt.title(f'Number of Data by {col}')
#  plt.xticks(rotation=60, fontsize=6)
#  plt.show()

# Order demand by each time unit
# for i, col in enumerate(cols_view):
#  data_grp = df.groupby(col, as_index=False)['Order_Demand'].sum()
#  plt.plot(data_grp[col], data_grp['Order_Demand'], label = col)
#  plt.title(f'Order Demand by {col}')
#  plt.xticks(rotation=60, fontsize=6)
#  plt.tight_layout()
#  plt.show()

# Order Demand Boxplot by Day of the Week
# df_view = df.copy().dropna()
# sns.boxplot(data = df_view, x='DayOW', y='Order_Demand')
# plt.show()

# # Order Demand by Time (Warehouse Perspective)
# cols_view = ['Year', 'Year_Month', 'Year_Week', 'Date']
# ls_wh = df['Warehouse'].unique()
#
# for col in cols_view:
#  data = df.groupby([col, 'Warehouse'], as_index=False)['Order_Demand']
#  od_sum = data.sum()
#  sns.lineplot(data= od_sum, x=col, y='Order_Demand', hue='Warehouse')
#  plt.legend()
#  plt.title(f'Total Order Demand by {col}')
#  plt.xticks(rotation=60, fontsize=6)
#  plt.show()


## Product Category Perspective
cols_view = ['Year', 'Year_Month', 'Year_Week', 'Date']
for col in cols_view:
 df_view = df.groupby([col, 'Product_Category'], as_index=False)['Order_Demand'].sum()
 sns.lineplot(data = df_view, x=col, y='Order_Demand', hue='Product_Category')
 plt.xticks(rotation=60, fontsize=8)
 plt.title(f'Product Category Demand by {col}')
 plt.legend()
 plt.show()