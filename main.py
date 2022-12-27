'''
https://www.kaggle.com/datasets/felixzhao/productdemandforecasting/code
'''

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
# exit()

# from autoviz import AutoViz_Class
# import sweetviz as sv

# if __name__ == '__main__':
df = pd.read_csv('./archive/Historical Product Demand.csv', parse_dates=['Date'])
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

# Order Demand
df['Order_Demand'] = df['Order_Demand'].replace('[)]', '', regex=True)
df['Order_Demand'] = df['Order_Demand'].replace('[(]', '-', regex=True)
df['Order_Demand'] = df['Order_Demand'].astype(int)

# print(df.dtypes)
# print(df.columns)

'''
Time Data 
'''
# df['Year'] = df['Date'].dt.year #연도
# df['Month'] = df['Date'].dt.month # 월
# df['Week'] = df['Date'].dt.isocalendar().week # 주 (week of the year)
# df['DayOW'] = df['Date'].dt.dayofweek #요일 (day of the week) FYI) Mon 0 - Sun = 6
# df['Year'] = df['Date'].dt.year.astype('Int16') #연도
# df['Month'] = df['Date'].dt.month.astype('Int16') # 월
# df['Week'] = df['Date'].dt.isocalendar().week # 주 (week of the year)
# df['DayOW'] = df['Date'].dt.dayofweek.astype('Int16') #요일 (day of the week) FYI) Mon 0 - Sun = 6

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
grp_byWH = df.groupby('Warehouse', as_index=False).agg({'Product_Code':['nunique'],
                                                        'Product_Category':['nunique'],
                                                        'Order_Demand':['sum', 'min', 'max', 'mean', 'median', 'std']})

# sns.boxplot(data = grp_byWH, x='Warehouse', y='Order_Demand')
# plt.show()
print(grp_byWH.T)
print(grp_byWH)
print(grp_byWH['Warehouse'])
print(grp_byWH['Order_Demand'])
print(grp_byWH['Order_Demand']['std'])
# grp_byPCAT['Demand_Proportion'] = (grp_byPCAT['Order_Demand']/grp_byPCAT['Order_Demand'].sum()) #전체 판매량의 기여도를 pct로 변환
# grp_byPCAT['Demand_Accumulated'] = grp_byPCAT['Demand_Proportion'].cumsum() #기여도 누적합계
# grp_byPCAT['Demand_80pct'] = 0
# grp_byPCAT.loc[grp_byPCAT['Demand_Accumulated'] <= 0.8, 'Demand_80pct'] = 1 #Demand 기여도 80%에 든다면 1로 표기
#
# print(grp_byPCAT)
# print(grp_byPCAT[grp_byPCAT['Demand_80pct'] == 1]['Product_Category'].unique())
# print(grp_byPCAT[grp_byPCAT['Demand_80pct'] == 1]['Product_Category'].nunique())
# print(grp_byPCAT['Product_Category'].nunique())
# print(grp_byPCAT[grp_byPCAT['Demand_80pct'] == 1]['Product_Category'].nunique() / grp_byPCAT['Product_Category'].nunique())


#
# # for col in ['Product_Category', 'Product_Code', 'Warehouse']:
# #  print(df[col].value_counts())
#
# AV = AutoViz_Class()
# AV.AutoViz(filename='', dfte= df, depVar = 'Order_Demand', verbose=2, max_rows_analyzed=df.shape[0], max_cols_analyzed=df.shape[1])
# print(df.dtypes)
#
# sv_report = sv.analyze(df)
# sv_report.show_html()
exit()

"""
결측치에서 패턴이 있을까?
"""


# 결측치만 모아둔 데이터 프레임 생성
df_null = df.copy()[df['Date'].isnull()]
# cnt_cols = len(df_null.columns)
# for i, col in enumerate(df_null.columns):
#     if col == 'Date': continue
#     plt.pie(df_null[col].value_counts(), labels = df_null[col].value_counts().index)
#     plt.title(f'Missing Values by {col}')
#     plt.legend(loc = 'upper right')
#     plt.show()

# 결측치: Order Demand 음수/양수 비율 확인하기
# df_null['Positive_Demand'] = 0
# df_null.loc[df_null['Order_Demand'] >= 0, 'Positive_Demand'] = 1
# plt.pie(df_null['Positive_Demand'].value_counts(), labels = df_null['Positive_Demand'].value_counts().index, autopct='%.0f')
# plt.legend()
# plt.title("Positive/Negative Demand Proportion")
# plt.show()


# 웨어하우스  A의 날짜 범위 확인
# print(df[df['Warehouse'] == 'Whse_A'].agg({'Date':['min', 'max', 'median', 'std']}))

# 웨어하우스 별 총 수량, 평균 수량, 표준편차
total_demand = df['Order_Demand'].sum()
for wh in df['Warehouse'].unique():
    wh_demand = df[df['Warehouse'] == wh]['Order_Demand'].sum()
    print(wh, wh_demand, f'({wh_demand/total_demand*100:.2f}%)')

# 웨어하우스 별 오더 총수량, 평균수량, 표준편차, 데이터 수
print(df.groupby(['Warehouse']).agg({'Order_Demand': ['sum', 'mean', 'std', 'count']}))

# 웨어하우스 별 오더 총수량, 평균수량, 표준편차, 데이터 수
print(df.groupby(['Warehouse']).agg({'Product_Code': ['nunique'], 'Product_Category':['nunique']}))

# 결측치 데이터 프레임 삭제
del df_null

# 웨어하우스 A의 데이터는 드랍
df = df.loc[df['Warehouse'] != "Whse_A"]
print(df.shape)




"""
Determine Product Range 
"""
# grp_byPC_


# print(df['Product_Code'].value_counts())
# print(df['Date'])



"""
### DUPLICATED - Date가 NaN인 Duplicated
# df_dupe = df.copy()[df.duplicated() & df['Date'].isnull()] # DF of dupes
# print(df_dupe['Product_Category'].unique())
# print(df_dupe['Product_Code'].unique())
# print(df_dupe.shape, df['Product_Category'].nunique())
# del df_dupe
"""
['Category_019' 'Category_005' 'Category_028' 'Category_006'
 'Category_026']
['Product_1464' 'Product_0428' 'Product_0417' 'Product_1416'
 'Product_0414' 'Product_0423' 'Product_0416' 'Product_1424'
 'Product_1539' 'Product_1420' 'Product_1421' 'Product_1423'
 'Product_1419' 'Product_1422' 'Product_1443' 'Product_1496'
 'Product_1548' 'Product_1541' 'Product_1368' 'Product_1388'
 'Product_1402' 'Product_1509' 'Product_1553' 'Product_1410'
 'Product_1284' 'Product_0020' 'Product_1299' 'Product_1560'
 'Product_0979' 'Product_1630' 'Product_1365' 'Product_1385'
 'Product_1276' 'Product_1427' 'Product_1535' 'Product_0643'
 'Product_1636' 'Product_1384' 'Product_0995' 'Product_0973'
 'Product_1432' 'Product_1445' 'Product_1441' 'Product_1442'
 'Product_1438' 'Product_1470' 'Product_0985' 'Product_0980'
 'Product_1409' 'Product_1563' 'Product_1622' 'Product_1007'
 'Product_0989' 'Product_1291' 'Product_1461' 'Product_1513'
 'Product_1250' 'Product_1669' 'Product_1908' 'Product_1293'
 'Product_0984' 'Product_0031' 'Product_0639' 'Product_1434'
 'Product_1448' 'Product_1444' 'Product_0421']

#Process finished with exit code 0

"""

### DUPLICATED - Date가 NaN이 아닌 Duplicated
# df_dupe = df.copy()[df.duplicated() & df['Date'].notnull()]  # DF of dupes
# # print(df_dupe[df['Product_Code'] == 'Product_0979'].sort_values(by=['Date']))
# df_prcd = df.copy()[~df.index.duplicated()]
# del df_dupe
"""