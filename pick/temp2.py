# 机器学习多因子选股——简单组合优化
# 实现了以下几种常见优化。首先设置我们的原始股票列表，以及定义一个函数返回该组资产过去  天的日收盘价序列。

import numpy as np   
import pandas as pd 
import scipy.optimize as sco
#universe = get_index_stocks('000300.XSHG')
# stock_list = universe[0:5]#为了方便演示这里只选取五只股票构建投资组合

'''给定股票列表得到过去245个交易日的收盘价面板'''
def get_closedata(stock_list):
    close_dict = {}
    for i in range(len(stock_list)):
        code_name = stock_list[i]
        # close_seq = attribute_history(stock_list[i],245,'1d', ('close'))
        close_seq = list(close_seq['close'])
        close_dict[code_name] = close_seq
        #transofrm to dataframe
    df_stock = pd.DataFrame(close_dict,columns = list(close_dict.keys()))
    return df_stock #255*N的DataFrame,每列对应一只股票过去245个交易日股价

# 最大化期望收益率

'''全局最大化期望收益率组合'''
def cal_expret(weights:list,df_stock):
    
    risk_free_rate = 0.03
    if len(weights) != df_stock.shape[1]:
        raise Exception("the weights should be same size as stock list")
    weights = np.array(weights/np.sum(weights))
    returns_daily = np.log(df_stock/df_stock.shift(1)).iloc[1:,:]
    expected_return = np.sum(returns_daily.mean()*weights)*244-risk_free_rate
    return expected_return
    
def max_expret(weight0:list,df_stock):
    
    stock_num = df_stock.shape[1]
    w_min = 1/(np.power(stock_num,1.5))
    w_max = 0.6
    df = df_stock
    def maxexpret(weights):
        return cal_expret(weights,df)*(-1) #minimize 
    cons = ({'type':'eq', 'fun':lambda x: np.sum(x)-1})
    bnds = tuple((w_min,w_max) for x in range(stock_num)) 
    optimize = sco.minimize(maxexpret, weight0 , method = 'SLSQP', bounds = bnds,constraints = cons)
    optim_weight = list(optimize['x'].round(4))
    
    return optim_weight

'''最大化夏普率组合'''
def cal_sharpe(weights:list,df_stock):
    
    risk_free_rate = 0.03
    if len(weights) != df_stock.shape[1]:
        raise Exception("the weights should be same size as stock list")
    weights = np.array(weights)/np.sum(weights)
    returns_daily = np.log(df_stock/df_stock.shift(1)).iloc[1:,:]
    expected_return = np.sum(returns_daily.mean()*weights)*244-risk_free_rate #annualized excess return
    Sigma = returns_daily.cov()*244
    Portfolio_vol = np.sqrt(np.dot(weights.T,np.dot(Sigma,weights)))
    Sharpe_ratio = expected_return/Portfolio_vol
    
    return Sharpe_ratio

def max_sharpe(weight0:list,df_stock):
   
    stock_num = df_stock.shape[1]
    w_min = 1/(np.power(stock_num,1.5))
    w_max = 0.5
    df = df_stock
    def maxsharpe(weights):
        return cal_sharpe(weights,df)*(-1)
    cons = ({'type':'eq', 'fun':lambda x: np.sum(x)-1}) #weights的求和=1
    bnds = tuple((w_min,w_max) for x in range(stock_num)) #w_i的上下限约束
    optimize = sco.minimize(maxsharpe,weight0,method = 'SLSQP',bounds = bnds, constraints = cons)
    optim_weight  = optimize['x'].round(4) 
    return optim_weight


'''效用函数最优化: 同时考虑期望收益率和组合风险'''
def cal_Utility(weights:list,df_stock,lambda_): #lambda 表示风险厌恶系数
    
    if len(weights) != df_stock.shape[1]:
        raise Exception("the weights should be same size as stock list")
    
    num = len(weights)
    weights = np.array(weights/np.sum(weights)) 
    #first part
    returns_daily = np.log(df_stock/df_stock.shift(1)).iloc[1:,:]
    first_part = np.sum(returns_daily.mean()*weights)*244
    #second part
    Sigma = returns_daily.cov()*244
    Portfolio_vol = np.sqrt(np.dot(weights.T,np.dot(Sigma,weights)))
    second_part = 0.5*lambda_*Portfolio_vol
    
    return first_part-second_part #w.T*return - 0.5*lambda*sigma
    
def max_utility(weight0:list,df_stock,lambda_):
    stock_num = df_stock.shape[1]
    w_min = 1/(np.power(stock_num,1.5))
    w_max = 1
    df = df_stock
    def maxutility(weights):
        return cal_Utility(weights,df,lambda_)*(-1)
    cons = ({'type':'eq', 'fun':lambda x: np.sum(x)-1}) #weights的求和=1
    bnds = tuple((w_min,w_max) for x in range(stock_num)) #w_i的上下限约束
    optimize = sco.minimize(maxutility,weight0,method = 'SLSQP',bounds = bnds, constraints = cons)
    optim_weight  = optimize['x'].round(4) 
    return optim_weight

'''风险平价:考虑不同个股之间的序列相关性'''
def RiskParityLoss(weights:list,df_stock):
    
    if len(weights) != df_stock.shape[1]:
        raise Exception("the weights should be same size as stock list")
        
    num = len(weights)
    weights = np.array(weights/np.sum(weights)) #normalizing
    #derive covariance matrix
    returns_daily = (np.log(df_stock/df_stock.shift(1))).iloc[1:,:]
    Sigma = returns_daily.cov()*244
    Portfolio_vol = np.sqrt(np.dot(weights.T,np.dot(Sigma,weights))) #组合波动率
    MRC = np.dot(Sigma,weights)/Portfolio_vol #边际风险贡献向量
    RC = MRC*weights #风险贡献
    RPLoss = 0
    for i in range(1,num):
        for j in range(i):
            RPLoss += (RC[i]-RC[j])**2
            
    return RPLoss
    
def Riskparity(weight0:list,df_stock):
    stock_num = df_stock.shape[1]
    df = df_stock
    def max_riskparity(weights):
        return RiskParityLoss(weights,df) #minimize 
    cons = ({'type':'eq', 'fun':lambda x: np.sum(x)-1}) #weights的求和=1
    bnds = tuple((0,1) for x in range(stock_num)) #风险平价只做(0,1)约束
    optimize = sco.minimize(max_riskparity, weight0 , method = 'SLSQP', bounds = bnds,constraints = cons)
    optim_weight = list(optimize['x'].round(4))
    return optim_weight


