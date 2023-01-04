import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import warnings
import pandas as pd
import tushare as ts
import numpy as np
import os
import datetime as dt
import scipy.stats as stats

ts.set_token('357f92fd3836f2d018d20b9b840897abb3e5c9a62e17895b413e05fe')
pro = ts.pro_api()

# 设置工作路径
os.getcwd() 
os.chdir('')

# 条件选股
result = pro.index_weight(index_code="399300.SZ",trade_date='20210901')
hs300 = result['con_code'].tolist()
hs300[:10]
#去掉股票代码中的市场信息
for i in range(len(hs300)):
    hs300[i] = hs300[i][0:6]
 
#获取基本面数据
# rev:收入同比（%）  profit:利润同比（%）    npr:净利润率（%）
stock_basics = pd.read_excel('data_1.xlsx',converters = {u'股票代码':str})  #为避免导入excel时省略股票代码前的0，这里用字符串形式代入
#stock_basics = ts.get_stock_basics()
#stock_basics.reset_index(inplace=True)
data1 = stock_basics.loc[stock_basics['股票代码'].isin(hs300),
                         ['股票代码','行业代码','行业名称','市盈率','市净率']]
#data1.columns = ['代码','名称','行业','PE','PB','EPS','收入%','利润%']
data1.head()
 
#获取盈利能力数据
stock_profit = pd.read_excel('data_2.xlsx',converters = {u'股票代码':str})
#stock_profit = ts.get_profit_data(2017,1)
data2 = stock_profit.loc[stock_profit['股票代码'].isin(hs300),['股票代码','ROE']]
#data2.columns = ['代码','ROE','毛利率','净利率']
#data2 = round(data2,2)
data2.head()
 
#其他数据（流动性指标、成长能力指标等）同理，这里只演示基本思路
 
#数据合并
#方法一
from functools import reduce
merge = lambda x,y: pd.merge(x,y,how='left',on='股票代码')   #定义了merge函数
data = reduce(merge,[data1,data2])  #reduce(fuction,sequence,start_value),对sequence中的数据迭代调用目标函数，相当于扩展了函数的参数个数
data.drop_duplicates(inplace=True)  #去除重复数据
data = data.fillna(0)
data.head()
#方法二
data3 = pd.merge(data1,data2,how='left', on='股票代码')
data3.head()
 
#根据已有列计算新数据
data['估值系数'] = data['市盈率'] * data['市净率']   #生成“烟蒂”，本杰明
#data = round(data,2)
data.head()
 
#多条件筛选
data_filtered = data.loc[(data['估值系数'] < 60) & (data['估值系数'] > 0) & (data['ROE']>0.1),
                         ['股票代码','行业代码','行业名称','市盈率','市净率','估值系数','ROE']]
print("筛选结果共 %d 只个股" % len(data_filtered))
 
#按选定字段对数据进行排序
data_filtered.sort_values(['估值系数'], ascending=True, inplace=True)
data_filtered.head(10)
 
#数据分类
def map_func(x):
    if x['ROE'] > 0.05:
        return '高成长'
    elif x['ROE'] >= 0:
        return '低成长'
    elif x['ROE'] < 0:
        return '亏损'
    
#根据ROE数据计算‘成长性’
data['成长性'] = data.apply(map_func, axis=1)  #将data代入目标函数，对每一行进行处理，并将函数的结果组合成一个series返回
data.head()
    
#对高成长分类按照‘烟蒂系数’做升序排列
data_growth = data[data['成长性'] == '高成长'].sort_values(['估值系数'],ascending=True)
data_growth.head()
 
#分类进行条件选股
data_grouped_2 = data.groupby('行业名称')
data_grouped_2.size()
 
def group_func(df):
    return df.sort_values(['估值系数'],ascending=True)[:2]
 
data_grouped = data.groupby('行业名称').apply(group_func)
data_grouped


