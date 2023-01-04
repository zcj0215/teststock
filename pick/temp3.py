""" 一个很实际的问题，在机器学习用于低频因子选股的时候，我不想在聚宽上爬数据+训练（当然可以在本地调用但是我还是懒），
但是如果在本地跑模型又会馋回测平台的方便，同时我也懒得用backtrader这种库。于是我借助Tushare和python实现了一个
等权的不考虑任何交易成本和持仓限制的简单回测框架——完全根据自定义的换仓频率，输出组合在回测期间的净值曲线的回测框架
——同时还附带了几个常见的评价指标。当然，基于这个版本后来我又设计了考虑commision和行业中性市值加权组合的回测框架。这篇文章谨记录简单的版本。


低频机器学习或者深度学习选股的逻辑很无脑，可以把全过程拆分成训练+回测两个部分。训练部分获取数据+训练。回测部分在换仓期使用模型输出个股的预测收益率，
排序并选头部的一揽子股票构建下个周期的持仓组合。这个简单的框架可以完成的功能包括：

可以灵活插入自定义的模型和方法（输入个股代码输出预测收益率）。
通过全局变量设置回测区间，调仓周期（以交易日为单位），选股数量，股票池，基准指数，初始本金。
可以筛选掉那些历史数据不完整的股票。
通过可视化模块绘制基准和投资组合的净值曲线，计算组合年化超额收益率，年化夏普率，最大回撤（动态规划的思想自定义计算最大回撤的函数）。
以最近自己实习在做的一个改进alphanet因子挖掘网络的project举例，在每个换仓日对每个个股我们获取其过去30天的9个价量指标，
通过自定义的信息提取层，卷积层，池化层和空间注意力机制来实现对个股价量背离因子（逻辑近似worldquant101）的挖掘并回归
预测后10个交易日（双周频）的收益率（具体细节就不展开说了），因此我们预测收益率输入的应该是9*30的二维数值矩阵。这也是我在框架主体里面使用了以下代码： """


import datetime
import math
import time
from datetime import timedelta #两个日期间隔
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

import tushare as ts
pro = ts.pro_api()
plt.style.use('science')
ts.set_token('357f92fd3836f2d018d20b9b840897abb3e5c9a62e17895b413e05fe')


start_date = '20200101' #回测起点
end_date = '20200630' #回测终点
sum_0 = 1000
frequency = 10 #换仓期
num_stock = 50 #头部选股数目
stock_pool = '399300.SZ' #股票池
benchmark = '399300.SZ'#指数benchmark
sum0 = sum_0 #初始本金：由于仅仅绘制净值曲线因此无所谓
portfolio_list = [] #组合净值列表


df_price = pro.daily(ts_code = code, #OHLC,pct_change,volume
                       start_date=start, end_date=date)
df_basic = pro.daily_basic(ts_code=code, #other features
                            start_date=start, end_date=date)
if (df_price.shape[0] == df_basic.shape[0]) & (df_price.shape[0] == len1): #判断数据的完整性
    df_price = df_price.iloc[1:pass_day+1,[2,3,4,5,8,9]].fillna(0.1)
    df_basic = df_basic.iloc[1:pass_day+1,[3,4,5]].fillna(0.1)
    data = np.array(pd.merge(df_price,df_basic,left_index=True,right_index=True).iloc[::-1].T)
    #这里需要经过模型输出得到收益率，这里先用随机数替代
    #这里定义一个方法使用训练完成的模型输出预测收益率

""" 这一段的代码读者可以根据自己的模型架构进行修改，总之只需要定义一个函数，输入当天交易日日期和个股代码能返回该股票收益率的预测值即可。
这里方便演示我直接使用0-1的随机数代替预测收益率。正式的演示如下：     """

#定义一个函数返回回测期间的交易日列表
def get_datelist(start:str,end:str):
    df = pro.index_daily(ts_code='399300.SZ',start_date= start, end_date= end)
    date_list = list(df.iloc[::-1]['trade_date'])
    return date_list

#返回交易日当天的len1
#这里的passday是用于模型输入的数据依赖窗口
def get_length(date:str,pass_day:int):
    start = str(pd.to_datetime(date)-timedelta(pass_day*2))
    start = start[0:4]+start[5:7]+start[8:10]
    len_1 = pro.index_daily(ts_code='399300.SZ',start_date=start,end_date=date).shape[0]
    return len_1

#返回交易日当天的股票池
def get_stocklist(date:str,stock_pool:str):
    start = str(pd.to_datetime(date)-timedelta(30))
    start = start[0:4]+start[5:7]+start[8:10]
    df1 =pro.index_weight(index_code = stock_pool,
                          start_date=start,end_date=date)#交易日当天的股票列表
    codes = list(df1['con_code'])[0:300] #取前300即是最新的成分股
    #该函数还可以返回成分股权重
    return codes

#计算最大回撤
def Maxdrawdown(Price:list): 
    Price = Price[::-1] #等价于求正序列的最大利润/price
    min_price = 10000000
    max_drawdown = 0
    for price in Price:
        min_price = min(min_price,price)
        max_drawdown = max(max_drawdown,(price-min_price)/price) 
    return max_drawdown*100

# 主框架算法
date_list = get_datelist(start_date,end_date)
for i in range(len(date_list)):
    if i % frequency == 0:
        range_list = date_list[i:i+frequency]
        length = len(range_list) #这里不一定是10
        date = range_list[0] #交易日当天
        end = range_list[-1] #区间最后一天
        num = 0
        value = np.zeros(length)
        factor_dict = {}
        pass_day = 30 #模型输入需要用到的过去的天数数据
        stock_list = get_stocklist(date,stock_pool)
        len1 = get_length(date,pass_day)
        start = str(pd.to_datetime(date)-timedelta(pass_day*2))
        start = start[0:4]+start[5:7]+start[8:10]
        #得到预测值
        #以下的for循环也可以根据自己的策略封装成方法，输入股票列表返回对应的合成因子字典
        for code in stock_list:
            df_price = pro.daily(ts_code = code, #OHLC,pct_change,volume
                       start_date=start, end_date=date)
            df_basic = pro.daily_basic(ts_code=code, #other features
                            start_date=start, end_date=date)
            if (df_price.shape[0] == df_basic.shape[0]) & (df_price.shape[0] == len1): #判断数据的完整性
                df_price = df_price.iloc[1:pass_day+1,[2,3,4,5,8,9]].fillna(0.1)
                df_basic = df_basic.iloc[1:pass_day+1,[3,4,5]].fillna(0.1)
                data = np.array(pd.merge(df_price,df_basic,left_index=True,right_index=True).iloc[::-1].T)
                #这里需要经过模型输出得到收益率，这里先用随机数替代
                #这里定义一个方法使用训练完成的模型输出预测收益率
                y_pred = np.random.random(1).round(2)[0]
                factor_dict[code] = y_pred
            time.sleep(0.5)
        return_df = pd.DataFrame(factor_dict.values(),
                         index=list(factor_dict.keys()),#按收益率预测值排序
                         columns=['pred_return']).sort_values(by = 'pred_return',ascending=False)
        selected_stock = list(return_df.index)[0:num_stock] #换仓股票
        for j in range(len(selected_stock)):
            code = selected_stock[j]
            df_return = pro.daily(ts_code = code,
                   start_date=date, end_date=end).iloc[::-1]['close'] #未来持仓期的价格序列
            if (df_return.shape[0] == length) : #判断数据完整
                df_return = np.array(df_return)
                df_return = df_return/df_return[0]
                value = value + df_return
                num+=1
            else:
                pass
        value = value/num
        value = value/value[0]*sum0
        turn_list = value.tolist() 
        for value_ in turn_list:
            portfolio_list.append(value_)
        period_return = value[-1]/value[0]-1#本期的收益率
        sum0 = sum0 * (1+period_return)#本期期末的总本金,下个期期初的净值
    else : 
        pass


# 策略结果可视化及评估

#得到基准指数的净值列表
df_bench = pro.index_daily(ts_code=benchmark,start_date = start_date, 
                         end_date=end_date).iloc[::-1].reset_index()[['trade_date','close']]
BM_value = np.array(df_bench['close'])
BM_value = BM_value/BM_value[0]*sum_0
#Visualization
with plt.style.context(['science','no-latex']):
    fig, ax = plt.subplots(figsize = (12,5)) 
    if len(portfolio_list) == len(BM_value):
        ax.plot(df_bench.trade_date, BM_value, linewidth =2, label = "Benchmark Index") #沪深300指数
        ax.plot(df_bench.trade_date, portfolio_list, linewidth =2, label = "Active Portfolio") #沪深300指数
        ax.legend(title = "Backtesing Result")
        ax.autoscale(tight = True)
        ax.set(xlabel = r'Date') #label使用latex语法
        ax.set(ylabel = 'Portfolio Value')
    else :
        raise Exception("the benchmark list is not the same size as porfolio list")
        
bactesting_days = len(portfolio_list) #回测区间长度
Total_days = 252
#年化超额收益
annualized_return = (portfolio_list[-1]/portfolio_list[0])**(252/bactesting_days)-1
annualized_Index = (BM_value[-1]/BM_value[0])**(252/bactesting_days)-1
annualized_excess_return = (annualized_return-annualized_Index)*100 #年化超额收益率百分比
#夏普比率
sigma = np.std(portfolio_list) * np.sqrt(252/bactesting_days) #年化波动率
sharpe_ratio = annualized_excess_return/(sigma) 
#最大回撤率
maximum_drawdown = Maxdrawdown(portfolio_list)
#打印指标
print("The annualized excess return:",np.round(annualized_excess_return,2),"%")
print("The sharpe ratio:",np.round(sharpe_ratio,2))
print("The maximum drawdown rate:",np.round(maximum_drawdown,2),"%")    