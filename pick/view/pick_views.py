from tkinter import EXCEPTION
import time
import talib
from  MyTT import *
import pandas as pd
from django.http import  HttpResponse

from astocks.models import Stocks,StockList,Stocksz,Stockszc,Stocksh,Stockshk,Stockbj,Stocksector

def calculate_CCI(data,n=14):
    
    cci = talib.CCI(data["high"].astype(float),data["low"].astype(float),data["close"].astype(float),timeperiod=n)
 
    return  cci

def calculate_KDJ(data,n=9,m1=3,m2=3):
    
    k,d = talib.STOCH(data["high"].astype(float),data["low"].astype(float),data["close"].astype(float),fastk_period=n,slowk_period=m1,slowd_period=m2)
    j = 3*d - 2*k
    
    return  k, d, j

def calculate_DMI(data,n=14,m=6):
    pdi = round(talib.PLUS_DI(data["high"].astype(float),data["low"].astype(float),data["close"].astype(float), timeperiod=n), 2)
    mdi = round(talib.MINUS_DI(data["high"].astype(float),data["low"].astype(float),data["close"].astype(float), timeperiod=n),2)
    adx = round(talib.ADX(data["high"].astype(float),data["low"].astype(float),data["close"].astype(float), timeperiod=m),2)
    adxr = round(talib.ADXR(data["high"].astype(float),data["low"].astype(float),data["close"].astype(float), timeperiod=m),2)

    return  pdi, mdi, adx, adxr

def mytt_DMI(data,n=14,m=6):
    CLOSE = data["close"].astype(float)
    HIGH = data["high"].astype(float)
    LOW = data["low"].astype(float)
    PDI, MDI, ADX, ADXR = DMI(CLOSE,HIGH,LOW,n,m)
    
    return PDI, MDI

def stock_select(request):
    stocks = StockList.objects.all().order_by('symbol')  
    
    selection = []
    jsonlist = []
    for stock in stocks:
        if stock.symbol == '000002':
           continue
        start = stock.list_date[:4]+'-'+stock.list_date[4:6]+'-'+stock.list_date[6:]
        end = time.strftime("%Y-%m-%d", time.localtime())
        if stock.ts_code[7:] == 'SZ':
            if stock.ts_code[:6][:2] == '30':  
              try:
                  data = Stockszc.objects.all().filter(date__range=[start,end],code=stock.ts_code[:6]).order_by('-date')
              
                  for row in data:
                      dict = {}
                      dict["name"] = stock.name
                      dict["code"] = str(row.code)
                      dict["open"] = str(row.open)
                      dict["close"] = str(row.close)
                      dict["low"] = str(row.low)
                      dict["high"] = str(row.high)
                      dict["vol"] = str(row.volume)
                      dict["change"] = str(row.price_change)
                      dict["pct_chg"] = str(row.p_change)
                      dict["amount"] = str(row.amount)
                      dict["pre_close"] = str(row.pre_close)
                      dict["turnover"] = str(row.turnover)
                      dict["trade_date"] = str(row.date)
                      dict["capital_inflow"] = str(row.capital_inflow)
                      print(dict)
                      jsonlist.append(dict) 
               
              except EXCEPTION:
                  pass
            else:
              try:
                  data = Stocksz.objects.all().filter(date__range=[start,end],code=stock.ts_code[:6]).order_by('-date')
              
                  for row in data:
                      dict = {}
                      dict["name"] = stock.name
                      dict["code"] = str(row.code)
                      dict["open"] = str(row.open)
                      dict["close"] = str(row.close)
                      dict["low"] = str(row.low)
                      dict["high"] = str(row.high)
                      dict["vol"] = str(row.volume)
                      dict["change"] = str(row.price_change)
                      dict["pct_chg"] = str(row.p_change)
                      dict["amount"] = str(row.amount)
                      dict["pre_close"] = str(row.pre_close)
                      dict["turnover"] = str(row.turnover)
                      dict["trade_date"] = str(row.date)
                      dict["capital_inflow"] = str(row.capital_inflow)  
                      print(dict)
                      jsonlist.append(dict) 
              
              except EXCEPTION:
                  pass
        elif stock.ts_code[7:] == 'SH':
            if stock.ts_code[:6][:2] == '68':  
              try:
                  data = Stockshk.objects.all().filter(date__range=[start,end],code=stock.ts_code[:6]).order_by('-date')
              
                  for row in data:
                      dict = {}
                      dict["name"] = stock.name
                      dict["code"] = str(row.code)
                      dict["open"] = str(row.open)
                      dict["close"] = str(row.close)
                      dict["low"] = str(row.low)
                      dict["high"] = str(row.high)
                      dict["vol"] = str(row.volume)
                      dict["change"] = str(row.price_change)
                      dict["pct_chg"] = str(row.p_change)
                      dict["amount"] = str(row.amount)
                      dict["pre_close"] = str(row.pre_close)
                      dict["turnover"] = str(row.turnover)
                      dict["trade_date"] = str(row.date)
                      dict["capital_inflow"] = str(row.capital_inflow) 
                      print(dict) 
                      jsonlist.append(dict) 
              
                     
              except EXCEPTION:
                  pass
            else:     
              try:
                  data = Stocksh.objects.all().filter(date__range=[start,end],code=stock.ts_code[:6]).order_by('-date')
              
                  for row in data:
                      dict = {}
                      dict["name"] = stock.name
                      dict["code"] = str(row.code)
                      dict["open"] = str(row.open)
                      dict["close"] = str(row.close)
                      dict["low"] = str(row.low)
                      dict["high"] = str(row.high)
                      dict["vol"] = str(row.volume)
                      dict["change"] = str(row.price_change)
                      dict["pct_chg"] = str(row.p_change)
                      dict["amount"] = str(row.amount)
                      dict["pre_close"] = str(row.pre_close)
                      dict["turnover"] = str(row.turnover)
                      dict["trade_date"] = str(row.date)
                      dict["capital_inflow"] = str(row.capital_inflow)  
                      print(dict)
                      jsonlist.append(dict) 
                    
              except EXCEPTION:
                  pass
        elif stock.ts_code[7:] == 'BJ':
          try:
              data = Stockbj.objects.all().filter(date__range=[start,end],code=stock.ts_code[:6]).order_by('-date')
              
              for row in data:
                  dict = {}
                  dict["name"] = stock.name
                  dict["code"] = str(row.code)
                  dict["open"] = str(row.open)
                  dict["close"] = str(row.close)
                  dict["low"] = str(row.low)
                  dict["high"] = str(row.high)
                  dict["vol"] = str(row.volume)
                  dict["change"] = str(row.price_change)
                  dict["pct_chg"] = str(row.p_change)
                  dict["amount"] = str(row.amount)
                  dict["pre_close"] = str(row.pre_close)
                  dict["turnover"] = str(row.turnover)
                  dict["trade_date"] = str(row.date)
                  dict["capital_inflow"] = str(row.capital_inflow)  
                  print(dict)
                  jsonlist.append(dict) 
                    
          except EXCEPTION:
              pass
        jsonlist.reverse()
        mypd = pd.DataFrame(jsonlist,columns=['name','code','open','close','low','high','vol','change','pct_chg','amount','pre_close','turnover','trade_date','capital_inflow'])
       
        signals = pd.DataFrame(index=mypd.index)
        pdi, mdi, adx, adxr = calculate_DMI(mypd)
        signals['pdi'] = pdi
        signals['mdi'] = mdi
        signals['adx'] = adx
        signals['adxr'] = adxr
        
        signals['mdibuy_signal'] = ((((signals['pdi'] > signals['mdi']) & (signals['pdi'].shift(1).fillna(method="ffill") < signals['mdi'].shift(1).fillna(method="ffill")) & (signals['mdi'] < 30)) |((signals['mdi'] < signals['adxr'])&(signals['mdi'].shift(1).fillna(method="ffill") > signals['adxr'].shift(1).fillna(method="ffill"))&(signals['pdi'] < signals['mdi'])&(signals['pdi'] < signals['adx'])&(signals['pdi'] < signals['adxr'])&(signals['pdi']>signals['pdi'].shift(1).fillna(method="ffill")) )| ((signals['adx'] < signals['adxr'])& (signals['adx'].shift(1).fillna(method="ffill") > signals['adxr'].shift(1).fillna(method="ffill"))&(signals['pdi'] < signals['mdi'])&(signals['pdi'] < signals['adx'])&(signals['pdi'] < signals['adxr'])&(signals['pdi'] > signals['pdi'].shift(1).fillna(method="ffill"))))).astype(int)

        print(signals['mdibuy_signal'].tolist() )
        if signals['mdibuy_signal'].iloc[0]==1:
            dict = {}
            dict["name"] = mypd["name"][0]
            dict["code"] = mypd["code"][0]
           
            print('选中',mypd["name"][0]+mypd["code"][0])
            selection.append(dict) 
            
        signals.drop(index=range(len(signals)))
       
    print(selection)
        
    return HttpResponse('执行完毕！')
