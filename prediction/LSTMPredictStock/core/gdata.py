from astocks.models import StockList,Stocksz,Stockszc,Stocksh,Stockshk,Stockbj
from .data_processor import DataBuild
import os
from tkinter import EXCEPTION
from django.shortcuts import get_object_or_404
import platform

sysstr = platform.system()

def g_single_data(path,code,flag,name): 
    jsonlist = []
    if flag == 'SZ':
        if code[:2] == '30':  
            try:
                data = Stockszc.objects.all().filter(code=code).order_by('date')
              
                for row in data:
                    dict = {}
                    dict["Date"] = str(row.date)
                    dict["Code"] = str(row.code)
                    dict["Name"] = name
                    dict["Open"] = str(row.open)
                    dict["Close"] = str(row.close)
                    dict["High"] = str(row.high)
                    dict["Low"] = str(row.low)
                    dict["Volume"] = str(row.volume)
                    dict["Turnover"] = str(row.turnover)
                    dict["Pchange"] = str(row.p_change)
                    
                    jsonlist.append(dict) 
               
            except EXCEPTION:
                pass
        else:
            try:
                data = Stocksz.objects.all().filter(code=code).order_by('date')
              
                for row in data:
                    dict = {}
                    dict["Date"] = str(row.date)
                    dict["Code"] = str(row.code)
                    dict["Name"] = name
                    dict["Open"] = str(row.open)
                    dict["Close"] = str(row.close)
                    dict["High"] = str(row.high)
                    dict["Low"] = str(row.low)
                    dict["Volume"] = str(row.volume)
                    dict["Turnover"] = str(row.turnover)
                    dict["Pchange"] = str(row.p_change)
                        
                    jsonlist.append(dict) 
              
            except EXCEPTION:
                pass
    elif flag == 'SH':
        if code[:2] == '68':  
            try:
                data = Stockshk.objects.all().filter(code=code).order_by('date')
              
                for row in data:
                    dict = {}
                    dict["Date"] = str(row.date)
                    dict["Code"] = str(row.code)
                    dict["Name"] = name
                    dict["Open"] = str(row.open)
                    dict["Close"] = str(row.close)
                    dict["High"] = str(row.high)
                    dict["Low"] = str(row.low)
                    dict["Volume"] = str(row.volume)
                    dict["Turnover"] = str(row.turnover)
                    dict["Pchange"] = str(row.p_change)
                    
                    jsonlist.append(dict) 
              
                     
            except EXCEPTION:
                pass
        else:     
            try:
                data = Stocksh.objects.all().filter(code=code).order_by('date')
              
                for row in data:
                    dict = {}
                    dict["Date"] = str(row.date)
                    dict["Code"] = str(row.code)
                    dict["Name"] = name
                    dict["Open"] = str(row.open)
                    dict["Close"] = str(row.close)
                    dict["High"] = str(row.high)
                    dict["Low"] = str(row.low)
                    dict["Volume"] = str(row.volume)
                    dict["Turnover"] = str(row.turnover)
                    dict["Pchange"] = str(row.p_change)
                    
                    jsonlist.append(dict) 
                    
            except EXCEPTION:
                pass
    elif flag == 'BJ':
            try:
                data = Stockbj.objects.all().filter(code=code).order_by('date')
              
                for row in data:
                    dict = {}
                    dict["Date"] = str(row.date)
                    dict["Code"] = str(row.code)
                    dict["Name"] = name
                    dict["Open"] = str(row.open)
                    dict["Close"] = str(row.close)
                    dict["High"] = str(row.high)
                    dict["Low"] = str(row.low)
                    dict["Volume"] = str(row.volume)
                    dict["Turnover"] = str(row.turnover)
                    dict["Pchange"] = str(row.p_change)
                    
                    jsonlist.append(dict) 
                    
            except EXCEPTION:
                pass

    headers = ['Date','Code','Name','Open','Close','High','Low','Volume','Turnover','Pchange']
    if(sysstr =="Windows"):
        filename = path + '\\' + code+'.csv'
        DataBuild(filename,headers,jsonlist)
    else:
        filename = path + '/' + code+'.csv'
        DataBuild(filename,headers,jsonlist)
         
def gdata(path,stock_code='0'):
    if stock_code=='0':
        queryset = StockList.objects.all().order_by('symbol')
        for item in queryset:
            code = item.ts_code[:6]
            flag = item.ts_code[7:]
            name = item.name 
            g_single_data(path,code,flag,name)

    else:
        stock = get_object_or_404(StockList, symbol=stock_code)
        code = stock.ts_code[:6]
        flag = stock.ts_code[7:]
        name = stock.name
        g_single_data(path,code,flag,name)

