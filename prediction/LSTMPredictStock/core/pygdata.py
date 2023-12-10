from astocks.models import StockList,Stocksz,Stockszc,Stocksh,Stockshk,Stockbj
from .data_processor import DataBuild
import os
from tkinter import EXCEPTION
from django.shortcuts import get_object_or_404
import platform
from datetime import datetime

sysstr = platform.system()

def g_single_data(path,code,flag,name): 
    print(path)
    print(code)
    print(flag)
    print(name)    
    jsonlist = []
    if flag == 'SZ':
        if code[:2] == '30':  
            try:
                data = Stockszc.objects.all().filter(code=code).order_by('date')
              
                for row in data:
                    dict = {}
                    dict["index_code"] = "sz"+str(row.code)
                    dict["date"] = str(row.date)[:4]+'/'+ str(row.date)[5:7]+'/'+str(row.date)[8:10]
                    dict["open"] = str(row.open)
                    dict["close"] = str(row.close)
                    dict["low"] = str(row.low)
                    dict["high"] = str(row.high)
                    dict["volume"] = str(row.volume)
                    dict["money"] = str(row.amount)
                    dict["change"] = str(row.price_change)
                    
                    jsonlist.append(dict) 
               
            except EXCEPTION:
                pass
        else:
            try:
                data = Stocksz.objects.all().filter(code=code).order_by('date')
              
                for row in data:
                    dict = {}
                    dict["index_code"] = "sz"+str(row.code)
                    dict["date"] = str(row.date)[:4]+'/'+ str(row.date)[5:7]+'/'+str(row.date)[8:10]
                    dict["open"] = str(row.open)
                    dict["close"] = str(row.close)
                    dict["low"] = str(row.low)
                    dict["high"] = str(row.high)
                    dict["volume"] = str(row.volume)
                    dict["money"] = str(row.amount)
                    dict["change"] = str(row.price_change)
                        
                    jsonlist.append(dict) 
              
            except EXCEPTION:
                pass
    elif flag == 'SH':
        if code[:2] == '68':  
            try:
                data = Stockshk.objects.all().filter(code=code).order_by('date')
              
                for row in data:
                    dict = {}
                    dict["index_code"] = "sh"+str(row.code)
                    dict["date"] = str(row.date)[:4]+'/'+ str(row.date)[5:7]+'/'+str(row.date)[8:10]
                    dict["open"] = str(row.open)
                    dict["close"] = str(row.close)
                    dict["low"] = str(row.low)
                    dict["high"] = str(row.high)
                    dict["volume"] = str(row.volume)
                    dict["money"] = str(row.amount)
                    dict["change"] = str(row.price_change)
                    
                    jsonlist.append(dict) 
              
                     
            except EXCEPTION:
                pass
        else:     
            try:
                data = Stocksh.objects.all().filter(code=code).order_by('date')
              
                for row in data:
                    dict = {}
                    dict["index_code"] = "sh"+str(row.code)
                    dict["date"] = str(row.date)[:4]+'/'+ str(row.date)[5:7]+'/'+str(row.date)[8:10]
                    dict["open"] = str(row.open)
                    dict["close"] = str(row.close)
                    dict["low"] = str(row.low)
                    dict["high"] = str(row.high)
                    dict["volume"] = str(row.volume)
                    dict["money"] = str(row.amount)
                    dict["change"] = str(row.price_change)
                    
                    jsonlist.append(dict) 
                    
            except EXCEPTION:
                pass
    elif flag == 'BJ':
            try:
                data = Stockbj.objects.all().filter(code=code).order_by('date')
              
                for row in data:
                    dict = {}
                    dict["index_code"] = "bj"+str(row.code)
                    dict["date"] = str(row.date)[:4]+'/'+ str(row.date)[5:7]+'/'+str(row.date)[8:10]
                    dict["open"] = str(row.open)
                    dict["close"] = str(row.close)
                    dict["low"] = str(row.low)
                    dict["high"] = str(row.high)
                    dict["volume"] = str(row.volume)
                    dict["money"] = str(row.amount)
                    dict["change"] = str(row.price_change)
                    
                    jsonlist.append(dict) 
                    
            except EXCEPTION:
                pass

    headers = ['index_code','date','open','close','low','high','volume','money','change']
    if(sysstr =="Windows"):
        filename = path + '\\py' + code+'.csv'
        DataBuild(filename,headers,jsonlist)
    else:
        filename = path + '/py' + code+'.csv'
        DataBuild(filename,headers,jsonlist)
         
def pygdata(path,stock_code='0'):
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

