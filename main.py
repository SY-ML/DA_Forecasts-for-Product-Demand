'''
https://www.kaggle.com/datasets/felixzhao/productdemandforecasting/code
'''

import pandas as pd
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt

# if __name__ == '__main__':
df = pd.read_csv('./archive/Historical Product Demand.csv', parse_dates=['Date'])

print(df.dtypes)
print(df.columns)

"""
1. EDA
"""
# profile = ProfileReport(df= df, explorative=True)
# profile.to_file('pd_profile.html')

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

Process finished with exit code 0

"""

### DUPLICATED - Date가 NaN이 아닌 Duplicated
# df_dupe = df.copy()[df.duplicated() & df['Date'].notnull()]  # DF of dupes
# # print(df_dupe[df['Product_Code'] == 'Product_0979'].sort_values(by=['Date']))
# df_prcd = df.copy()[~df.index.duplicated()]
# del df_dupe

# 결측치에서 패턴이 있을까?


"""
Data Conversion
"""
# Order Demand: Str >> Int
df['Order_Demand'] = df['Order_Demand'].replace('[)]', '', regex=True)
df['Order_Demand'] = df['Order_Demand'].replace('[(]', '-', regex=True)
df['Order_Demand'] = df['Order_Demand'].astype(int)

### 주기 패턴이 있는지 확인
# df_1464 = df.copy()[df['Product_Code'] == 'Product_1464'].sort_values(by=['Date'])
# plt.scatter(x = df_1464['Date'], y = df_1464['Order_Demand'])
# plt.show()
# print(df_1464)

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



#
#
# print(df[df['Order_Demand']<0])
# mask_digit = df[df['Order_Demand'].str.isnumeric() == True]
# mask_alpha = df[df['Order_Demand'].str.isnumeric() == False]
# mask_digit = df[df['Order_Demand'].str.isdigit() == True]
# mask_alpha = df[df['Order_Demand'].str.isdigit() == False]
# print(mask_digit)
# print(mask_alpha)


"""
Determine Product Range 
"""
# grp_


# print(df['Product_Code'].value_counts())
# print(df['Date'])
