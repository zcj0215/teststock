from django.shortcuts import render

# Create your views here.
import os
from astocks.models import Stocksz,Stockszc,Stocksh,Stockshk,Stockbj,Stocks,Stocksector,StockChoose,StockLimitup,Stockindex
from boards.models import Board,BoardType
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from .forms import CodeForm
import platform
from django.db.models import Q
from django.db.models import Sum

import pandas as pd

from functools import wraps

sysstr = platform.system()

def prevent_duplicate_calls(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, '_prevent_duplicate_calls'):
            request._prevent_duplicate_calls = []
        
        if view_func in request._prevent_duplicate_calls:
            # 视图函数已经被调用过，返回一个合适的响应或错误
            return HttpResponse("Function already called for this session.", status=400)
        else:
            # 将视图函数添加到会话标记列表中
            request._prevent_duplicate_calls.append(view_func)
            # 调用视图函数
            response = view_func(request, *args, **kwargs)
            # 视图函数调用完毕后，可以移除它的标记
            request._prevent_duplicate_calls.remove(view_func)
            return response
    
    return wrapper

def readfile(mfn):
    '''
    以“只读”⽅式打开⽂件，读取文件所有行(直到结束符 EOF)
    :param mfn: 文件路经与文件名
    :return: 返回列表数据类型
    '''
    fp=open(mfn,'r',encoding='gbk')
    wls = fp.readlines()     #readlines把文本文件按行分割，并产生一个以每一行文本为一个元素的列表
    fp.close()
    return wls

def writefile(mfn,words):
    '''
    以“只写”⽅式打开⽂件,如有旧文件则替换
    :param mfn: 文件路经与文件名
    :param words: 字符串序列
    :return: 无返回值
    '''
    fp = open(mfn, 'w',encoding ='gbk')
    fp.writelines(words+'\n')
    fp.close()

def appendfile(mfn,str):
    '''
    以“只写”⽅式打开⽂件,文件指针指向文件尾，便于添加操作
    :param mfn: 文件路经与文件名
    :param str: 字符串序列
    :return: 无返回值
    '''
    fp = open(mfn, 'a',encoding ='gbk')
    fp.writelines(str+'\n')
    fp.close()
    
def turnover(code,flag,dd,amount,dt):
    if flag == 'SZ':
        if code[:2] == '30':  
            try:
                stock = get_object_or_404(Stockszc, code=code,date=dt)
                stock.turnover = float(dd)
                if amount !=0:
                    stock.amount = amount
                stock.save()
            except Http404:
                pass
        else:
            try:
                stock = get_object_or_404(Stocksz, code=code,date=dt)
                stock.turnover = float(dd)
                if amount !=0:
                    stock.amount = amount
                
                stock.save()
            except Http404:
                pass
    elif flag == 'SH':
        if code[:2] == '68':  
            try:
                stock = get_object_or_404(Stockshk, code=code,date=dt)
                stock.turnover = float(dd)
                if amount !=0:
                    stock.amount = amount
                stock.save()
            except Http404:
                pass
        else:     
            try:
                stock = get_object_or_404(Stocksh, code=code,date=dt)
                stock.turnover = float(dd)
                if amount !=0:
                    stock.amount = amount
                stock.save()
            except Http404:
                pass
    elif flag == 'BJ':
            try:
                stock = get_object_or_404(Stockbj, code=code,date=dt)
                stock.turnover = float(dd)
                if amount !=0:
                    stock.amount = amount
                stock.save()
            except Http404:
                pass


def everyday(code,open,close,high,low,volume,amount,turnover,volume_ratio,p_change,price_change,pre_close,pe,committee,dt):
    
    try:
        stock = get_object_or_404(Stocks, code=code)
        stock.growth = round(float(p_change),2)
        stock.committee = round(float(committee),2)
        stock.save()
    except Http404:
        pass
    
    try:
        stocks = StockChoose.objects.filter(code=code)
        if stocks:
            for stock in stocks:
                stock.growth = round(float(p_change),2)
                stock.save()
    except Http404:
        pass
    
    try:
        stocks = StockLimitup.objects.filter(code=code)
        if stocks:
            for stock in stocks:
                stock.growth = round(float(p_change),2)
                stock.save()
    except Http404:
        pass
    

    if code[:2] == '30':  
        try:
            stock = get_object_or_404(Stockszc, code=code,date=dt)
            stock.open = round(float(open),2)
            stock.high = round(float(high),2)
            stock.close = round(float(close),2)
            stock.pre_close = round(float(pre_close),2)
            stock.low = round(float(low),2)
            stock.volume = volume
            stock.amount = amount
            stock.turnover = round(float(turnover),2)
            stock.price_change = round(float(price_change),2)
            stock.p_change = round(float(p_change),2)
            stock.volume_ratio = round(float(volume_ratio),2)
            stock.pe = round(float(pe),2)
            stock.committee = round(float(committee),2)
            stock.save()
        except Http404:
            stock = Stockszc.objects.create(
                code = code,
                open = round(float(open),2),
                high = round(float(high),2),
                close = round(float(close),2),
                pre_close = round(float(pre_close),2),
                low = round(float(low),2),
                volume = volume,
                amount = amount,
                turnover = round(float(turnover),2),
                price_change = round(float(price_change),2),
                p_change = round(float(p_change),2),
                date = dt,
                volume_ratio = round(float(volume_ratio),2),
                pe = round(float(pe),2),
                committee = round(float(committee),2)
            )
    elif code[:2] == '00':
        try:
            stock = get_object_or_404(Stocksz, code=code,date=dt)
            stock.open = round(float(open),2)
            stock.high = round(float(high),2)
            stock.close = round(float(close),2)
            stock.pre_close = round(float(pre_close),2)
            stock.low = round(float(low),2)
            stock.volume = volume
            stock.amount = amount
            stock.turnover = round(float(turnover),2)
            stock.price_change = round(float(price_change),2)
            stock.p_change = round(float(p_change),2)
            stock.volume_ratio = round(float(volume_ratio),2)
            stock.pe = round(float(pe),2)
            stock.committee = round(float(committee),2)
            stock.save()
        except Http404:
            stock = Stocksz.objects.create(
                code = code,
                open = round(float(open),2),
                high = round(float(high),2),
                close = round(float(close),2),
                pre_close = round(float(pre_close),2),
                low = round(float(low),2),
                volume = volume,
                amount = amount,
                turnover = round(float(turnover),2),
                price_change = round(float(price_change),2),
                p_change = round(float(p_change),2),
                date = dt,
                volume_ratio = round(float(volume_ratio),2),
                pe = round(float(pe),2),
                committee = round(float(committee),2)
            )
    elif code[:2] == '68':
        try:
            stock = get_object_or_404(Stockshk, code=code,date=dt)   
            stock.open = round(float(open),2)
            stock.high = round(float(high),2)
            stock.close = round(float(close),2)
            stock.pre_close = round(float(pre_close),2)
            stock.low = round(float(low),2)
            stock.volume = volume
            stock.amount = amount
            stock.turnover = round(float(turnover),2)
            stock.price_change = round(float(price_change),2)
            stock.p_change = round(float(p_change),2)
            stock.volume_ratio = round(float(volume_ratio),2)
            stock.pe = round(float(pe),2)
            stock.committee = round(float(committee),2)
            stock.save()   
        except Http404:
            stock = Stockshk.objects.create(
                code = code,
                open = round(float(open),2),
                high = round(float(high),2),
                close = round(float(close),2),
                pre_close = round(float(pre_close),2),
                low = round(float(low),2),
                volume = volume,
                amount = amount,
                turnover = round(float(turnover),2),
                price_change = round(float(price_change),2),
                p_change = round(float(p_change),2),
                date = dt,
                volume_ratio = round(float(volume_ratio),2),
                pe = round(float(pe),2),
                committee = round(float(committee),2)
            ) 
    elif code[:2] == '60':    
        try:
            stock = get_object_or_404(Stocksh, code=code,date=dt)
            stock.open = round(float(open),2)
            stock.high = round(float(high),2)
            stock.close = round(float(close),2)
            stock.pre_close = round(float(pre_close),2)
            stock.low = round(float(low),2)
            stock.volume = volume
            stock.amount = amount
            stock.turnover = round(float(turnover),2)
            stock.price_change = round(float(price_change),2)
            stock.p_change = round(float(p_change),2)
            stock.volume_ratio = round(float(volume_ratio),2)
            stock.pe = round(float(pe),2)
            stock.committee = round(float(committee),2)
            stock.save()
        except Http404:
            stock = Stocksh.objects.create(
                code = code,
                open = round(float(open),2),
                high = round(float(high),2),
                close = round(float(close),2),
                pre_close = round(float(pre_close),2),
                low = round(float(low),2),
                volume = volume,
                amount = amount,
                turnover = round(float(turnover),2),
                price_change = round(float(price_change),2),
                p_change = round(float(p_change),2),
                date = dt,
                volume_ratio = round(float(volume_ratio),2),
                pe = round(float(pe),2),
                committee = round(float(committee),2)
            )
    else:
        try:
            stock = get_object_or_404(Stockbj, code=code,date=dt)
            stock.open = round(float(open),2)
            stock.high = round(float(high),2)
            stock.close = round(float(close),2)
            stock.pre_close = round(float(pre_close),2)
            stock.low = round(float(low),2)
            stock.volume = volume
            stock.amount = amount
            stock.turnover = round(float(turnover),2)
            stock.price_change = round(float(price_change),2)
            stock.p_change = round(float(p_change),2)
            stock.volume_ratio = round(float(volume_ratio),2)
            stock.pe = round(float(pe),2)
            stock.committee = round(float(committee),2)
            stock.save()
        except Http404:
            stock = Stockbj.objects.create(
                code = code,
                open = round(float(open),2),
                high = round(float(high),2),
                close = round(float(close),2),
                pre_close = round(float(pre_close),2),
                low = round(float(low),2),
                volume = volume,
                amount = amount,
                turnover = round(float(turnover),2),
                price_change = round(float(price_change),2),
                p_change = round(float(p_change),2),
                date = dt,
                volume_ratio = round(float(volume_ratio),2),
                pe = round(float(pe),2),
                committee = round(float(committee),2)
            )

def everyday_pe(code,turnover,volume_ratio,pe,committee,dt):

    if code[:2] == '30':  
        try:
            stock = get_object_or_404(Stockszc, code=code,date=dt)
            stock.turnover = round(float(turnover),2)
            stock.volume_ratio = round(float(volume_ratio),2)
            stock.pe = round(float(pe),2)
            stock.committee = round(float(committee),2)
            stock.save()
        except Http404:
           pass
    elif code[:2] == '00':
        try:
            stock = get_object_or_404(Stocksz, code=code,date=dt)
            stock.turnover = round(float(turnover),2)
            stock.volume_ratio = round(float(volume_ratio),2)
            stock.pe = round(float(pe),2)
            stock.committee = round(float(committee),2)
            stock.save()
        except Http404:
            pass
    elif code[:2] == '68':
        try:
            stock = get_object_or_404(Stockshk, code=code,date=dt)   
            stock.turnover = round(float(turnover),2)
            stock.volume_ratio = round(float(volume_ratio),2)
            stock.pe = round(float(pe),2)
            stock.committee = round(float(committee),2)
            stock.save()   
        except Http404:
            pass
    elif code[:2] == '60':    
        try:
            stock = get_object_or_404(Stocksh, code=code,date=dt)
            stock.turnover = round(float(turnover),2)
            stock.volume_ratio = round(float(volume_ratio),2)
            stock.pe = round(float(pe),2)
            stock.committee = round(float(committee),2)
            stock.save()
        except Http404:
          pass
    else:
        try:
            stock = get_object_or_404(Stockbj, code=code,date=dt)
            stock.turnover = round(float(turnover),2)
            stock.volume_ratio = round(float(volume_ratio),2)
            stock.pe = round(float(pe),2)
            stock.committee = round(float(committee),2)
            stock.save()
        except Http404:
            pass
            
def everyday_inflow0(code,inflow,dt):
    
    if code[:2] == '30':  
        try:
            stock = get_object_or_404(Stockszc, code=code,date=dt)
            stock.capital_inflow = inflow
            stock.save()
        except Http404:
            pass
    elif code[:2] == '00':
        try:
            stock = get_object_or_404(Stocksz, code=code,date=dt)
            stock.capital_inflow = inflow
            stock.save()
        except Http404:
            pass
    elif code[:2] == '68':
        try:
            stock = get_object_or_404(Stockshk, code=code,date=dt)
            stock.capital_inflow = inflow
            stock.save()   
        except Http404:
            pass
    elif code[:2] == '60':    
        try:
            stock = get_object_or_404(Stocksh, code=code,date=dt)
            stock.capital_inflow = inflow
            stock.save()
        except Http404:
            pass
    else:
        try:
            stock = get_object_or_404(Stockbj, code=code,date=dt)
            stock.capital_inflow = inflow
            stock.save()
        except Http404:
            pass
        
def everyday_nf(code,nf,dt):
    
    if code[:2] == '30':  
        try:
            stock = get_object_or_404(Stockszc, code=code,date=dt)
            stock.nf = nf
            stock.save()
        except Http404:
            pass
    elif code[:2] == '00':
        try:
            stock = get_object_or_404(Stocksz, code=code,date=dt)
            stock.nf = nf
            stock.save()
        except Http404:
            pass
    elif code[:2] == '68':
        try:
            stock = get_object_or_404(Stockshk, code=code,date=dt)
            stock.nf = nf
            stock.save()   
        except Http404:
            pass
    elif code[:2] == '60':    
        try:
            stock = get_object_or_404(Stocksh, code=code,date=dt)
            stock.nf = nf
            stock.save()
        except Http404:
            pass
    else:
        try:
            stock = get_object_or_404(Stockbj, code=code,date=dt)
            stock.nf = nf
            stock.save()
        except Http404:
            pass
        
def everyday_stockpe(code,pe,dt):
    
    if code[:2] == '30':  
        try:
            stock = get_object_or_404(Stockszc, code=code,date=dt)
            stock.pe = pe
            stock.save()
        except Http404:
            pass
    elif code[:2] == '00':
        try:
            stock = get_object_or_404(Stocksz, code=code,date=dt)
            stock.pe = pe
            stock.save()
        except Http404:
            pass
    elif code[:2] == '68':
        try:
            stock = get_object_or_404(Stockshk, code=code,date=dt)
            stock.pe = pe
            stock.save()   
        except Http404:
            pass
    elif code[:2] == '60':    
        try:
            stock = get_object_or_404(Stocksh, code=code,date=dt)
            stock.pe = pe
            stock.save()
        except Http404:
            pass
    else:
        try:
            stock = get_object_or_404(Stockbj, code=code,date=dt)
            stock.pe = pe
            stock.save()
        except Http404:
            pass

def everyday_inflow(code,inflow,dt,turnover):
    
    if code[:2] == '30':  
        try:
            stock = get_object_or_404(Stockszc, code=code,date=dt)
            stock.turnover = turnover
            stock.capital_inflow = inflow
            stock.save()
        except Http404:
            pass
    elif code[:2] == '00':
        try:
            stock = get_object_or_404(Stocksz, code=code,date=dt)
            stock.turnover = turnover
            stock.capital_inflow = inflow
            stock.save()
        except Http404:
            pass
    elif code[:2] == '68':
        try:
            stock = get_object_or_404(Stockshk, code=code,date=dt)
            stock.turnover = turnover   
            stock.capital_inflow = inflow
            stock.save()   
        except Http404:
            pass
    elif code[:2] == '60':    
        try:
            stock = get_object_or_404(Stocksh, code=code,date=dt)
            stock.turnover = turnover
            stock.capital_inflow = inflow
            stock.save()
        except Http404:
            pass
    else:
        try:
            stock = get_object_or_404(Stockbj, code=code,date=dt)
            stock.turnover = turnover
            stock.capital_inflow = inflow
            stock.save()
        except Http404:
            pass
    

def everyday_block(code,name,open,close,high,low,volume,tover,volume_ratio,pre_close,limitup_number,growth,growth_pre,growth_3,growth_fall,Continuerise_30_limitup,Continuerise_days,pe,dt):
    try:
        block = get_object_or_404(Stocksector,code=code,date=dt)
        block.open = round(float(open),2)
        block.high = round(float(high),2)
        block.close = round(float(close),2)
        block.pre_close = round(float(pre_close),2)
        block.low = round(float(low),2)
        block.volume = volume
        block.turnover = round(float(tover),2)
        block.volume_ratio = round(float(volume_ratio),2)
        block.limitup_number = round(float(limitup_number),2)
        block.growth = round(float(growth),2)
        block.growth_pre = round(float(growth_pre),2)
        block.growth_3 = round(float(growth_3),2)
        block.growth_fall = growth_fall
        block.Continuerise_30_limitup = round(float(Continuerise_30_limitup),2)
        block.Continuerise_days = round(float(Continuerise_days),2)
        block.name = name
        if str(pe).lstrip().rstrip() != '--':
            block.pe = round(float(pe),2)
        block.save()
    except Http404:
        if str(pe).lstrip().rstrip() != '--':
            block = Stocksector.objects.create(
                code = code,
                name = name,
                open = round(float(open),2),
                high = round(float(high),2),
                close = round(float(close),2),
                pre_close = round(float(pre_close),2),
                low = round(float(low),2),
                volume = volume,
                turnover = round(float(tover),2),
                volume_ratio = round(float(volume_ratio),2),
                limitup_number = round(float(limitup_number),2),
                growth = round(float(growth),2),
                growth_pre = round(float(growth_pre),2),
                growth_3 = round(float(growth_3),2),
                growth_fall = growth_fall,
                Continuerise_30_limitup = round(float(Continuerise_30_limitup),2),
                Continuerise_days = round(float(Continuerise_days),2),
                date = dt,
                pe = round(float(pe),2)
            )
        else:
            block = Stocksector.objects.create(
                code = code,
                name = name,
                open = round(float(open),2),
                high = round(float(high),2),
                close = round(float(close),2),
                pre_close = round(float(pre_close),2),
                low = round(float(low),2),
                volume = volume,
                turnover = round(float(tover),2),
                volume_ratio = round(float(volume_ratio),2),
                limitup_number = round(float(limitup_number),2),
                growth = round(float(growth),2),
                growth_pre = round(float(growth_pre),2),
                growth_3 = round(float(growth_3),2),
                growth_fall = growth_fall,
                Continuerise_30_limitup = round(float(Continuerise_30_limitup),2),
                Continuerise_days = round(float(Continuerise_days),2),
                date = dt     
            )    
        
def everyday_blockpe(code,pe,dt):
    try:
        block = get_object_or_404(Stocksector,code=code,date=dt)
        if str(pe).lstrip().rstrip() != '--':
            block.pe = round(float(pe),2)
        block.save()
    except Http404:
        pass
        
def block_history(code,name,open,close,high,low,volume,dt):
    try:
        block = get_object_or_404(Stocksector,code=code,date=dt)
        block.open = round(float(open),2)
        block.high = round(float(high),2)
        block.close = round(float(close),2)
        block.low = round(float(low),2)
        block.volume = volume
        block.name = name
        block.save()
    except Http404:
        block = Stocksector.objects.create(
                code = code,
                name = name,
                open = round(float(open),2),
                high = round(float(high),2),
                close = round(float(close),2),
                low = round(float(low),2),
                volume = volume,
                date = dt     
        )
        
def everyday_index(code,name,open,close,high,low,volume,amount,price_change,growth,amplitude,dt):
    try:
        block = get_object_or_404(Stockindex,code=code,date=dt)
        block.open = round(float(open),2)
        block.high = round(float(high),2)
        block.low = round(float(low),2)
        block.close = round(float(close),2)
        block.volume = volume
        block.amount = amount
        block.price_change = round(float(price_change),2)
        block.growth = round(float(growth),2)
        block.amplitude = round(float(amplitude),2)
        block.name = name
        block.save()
    except Http404:
        block = Stockindex.objects.create(
                code = code,
                name = name,
                open = round(float(open),2),
                high = round(float(high),2),
                close = round(float(close),2),
                low = round(float(low),2),
                volume = volume,
                amount = amount,
                price_change = round(float(price_change),2),
                growth = round(float(growth),2),
                amplitude = round(float(amplitude),2),
                date = dt     
        )
 
def everyday_indexpe(code,pe,dt):
    try:
        block = get_object_or_404(Stockindex,code=code,date=dt)
        block.pe = round(float(pe),2)
        block.save()
    except Http404:
       pass
    
def everydayout(dt):
    path =  os.path.dirname(__file__)   
    if(sysstr =="Windows"):
        filename = path+"\\Table.txt"
    else:
        filename = path+"/Table.txt"


    head = '代码      开盘       最新       最高       最低       总量       金额      换手%    量比     涨幅%     涨跌      昨收'
    print(head)
    writefile(filename, head)
    
    stocks = Stocksz.objects.all().filter(date=dt)
    for row in  stocks:
        dict = {}
        dict["code"] = str(row.code)
        dict["open"] = str(row.open)
        dict["close"] = str(row.close)
        dict["high"] = str(row.high)
        dict["low"] = str(row.low)
        dict["vol"] = str(row.volume)
        dict["amount"] = str(row.amount)
        dict["turnover"] = str(row.turnover)
        dict["volume_ratio"] = str(row.volume_ratio)
        dict["p_chg"] = str(row.p_change)
        dict["price_change"] = str(row.price_change)
        dict["pre_close"] = str(row.pre_close)
                  
        item_list = [dict["code"],dict["open"],dict["close"], dict["high"],dict["low"],dict["vol"],dict["amount"],dict["turnover"],dict["volume_ratio"], dict["p_chg"],dict["price_change"],dict["pre_close"]]
        item_str = '    '.join(item_list)
        print(item_str)
        appendfile(filename, item_str)

    stocks = Stockszc.objects.all().filter(date=dt)
    for row in  stocks:
        dict = {}
        dict["code"] = str(row.code)
        dict["open"] = str(row.open)
        dict["close"] = str(row.close)
        dict["high"] = str(row.high)
        dict["low"] = str(row.low)
        dict["vol"] = str(row.volume)
        dict["amount"] = str(row.amount)
        dict["turnover"] = str(row.turnover)
        dict["volume_ratio"] = str(row.volume_ratio)
        dict["p_chg"] = str(row.p_change)
        dict["price_change"] = str(row.price_change)
        dict["pre_close"] = str(row.pre_close)
                  
        item_list = [dict["code"],dict["open"],dict["close"], dict["high"],dict["low"],dict["vol"],dict["amount"],dict["turnover"],dict["volume_ratio"], dict["p_chg"],dict["price_change"],dict["pre_close"]]
        item_str = '    '.join(item_list)
        print(item_str)
        appendfile(filename, item_str)

    stocks = Stocksh.objects.all().filter(date=dt)
    for row in  stocks:
        dict = {}
        dict["code"] = str(row.code)
        dict["open"] = str(row.open)
        dict["close"] = str(row.close)
        dict["high"] = str(row.high)
        dict["low"] = str(row.low)
        dict["vol"] = str(row.volume)
        dict["amount"] = str(row.amount)
        dict["turnover"] = str(row.turnover)
        dict["volume_ratio"] = str(row.volume_ratio)
        dict["p_chg"] = str(row.p_change)
        dict["price_change"] = str(row.price_change)
        dict["pre_close"] = str(row.pre_close)
                  
        item_list = [dict["code"],dict["open"],dict["close"], dict["high"],dict["low"],dict["vol"],dict["amount"],dict["turnover"],dict["volume_ratio"], dict["p_chg"],dict["price_change"],dict["pre_close"]]
        item_str = '    '.join(item_list)
        print(item_str)
        appendfile(filename, item_str) 

    stocks = Stockshk.objects.all().filter(date=dt)
    for row in  stocks:
        dict = {}
        dict["code"] = str(row.code)
        dict["open"] = str(row.open)
        dict["close"] = str(row.close)
        dict["high"] = str(row.high)
        dict["low"] = str(row.low)
        dict["vol"] = str(row.volume)
        dict["amount"] = str(row.amount)
        dict["turnover"] = str(row.turnover)
        dict["volume_ratio"] = str(row.volume_ratio)
        dict["p_chg"] = str(row.p_change)
        dict["price_change"] = str(row.price_change)
        dict["pre_close"] = str(row.pre_close)
                  
        item_list = [dict["code"],dict["open"],dict["close"], dict["high"],dict["low"],dict["vol"],dict["amount"],dict["turnover"],dict["volume_ratio"], dict["p_chg"],dict["price_change"],dict["pre_close"]]
        item_str = '    '.join(item_list)
        print(item_str)
        appendfile(filename, item_str)  

    stocks = Stockbj.objects.all().filter(date=dt)
    for row in  stocks:
        dict = {}
        dict["code"] = str(row.code)
        dict["open"] = str(row.open)
        dict["close"] = str(row.close)
        dict["high"] = str(row.high)
        dict["low"] = str(row.low)
        dict["vol"] = str(row.volume)
        dict["amount"] = str(row.amount)
        dict["turnover"] = str(row.turnover)
        dict["volume_ratio"] = str(row.volume_ratio)
        dict["p_chg"] = str(row.p_change)
        dict["price_change"] = str(row.price_change)
        dict["pre_close"] = str(row.pre_close)
                  
        item_list = [dict["code"],dict["open"],dict["close"], dict["high"],dict["low"],dict["vol"],dict["amount"],dict["turnover"],dict["volume_ratio"], dict["p_chg"],dict["price_change"],dict["pre_close"]]
        item_str = '    '.join(item_list)
        print(item_str)
        appendfile(filename, item_str)          


def home(request):
    return HttpResponse('选股！')            

def query(request):
    path =  os.path.dirname(__file__)
    fl = []
    if(sysstr =="Windows"):
        filename = path+"\\Table.txt"
        fl = readfile(filename)
    else:
        filename = path+"/Table.txt"
        fl = readfile(filename)
    
    data_temp = []
    data_list = []
    for item in fl:
        if item[0:3] != '时间' and item[0:1] != '':
            if len(item) > 10:
                data_temp = item.split('\t')
                data_list.append([data_temp[0][0:10],data_temp[1]])


    for data in data_list:
        turnover('000636','SZ',data[1], data[0])

    return HttpResponse('执行完毕！')

def jquery(request):
    path =  os.path.dirname(__file__)
    fl = []
    if(sysstr =="Windows"):
        filename = path+"\\Table.txt"
        fl = readfile(filename)
    else:
        filename = path+"/Table.txt"
        fl = readfile(filename)
    
    data_temp = []
    data_list = []
    for item in fl:
        if item[0:2] != '代码':
            if len(item) > 9:
                data_temp = item.split('    ')
                data_list.append([data_temp[0][0:6],data_temp[1]])


    for data in data_list:
        turnover(data[0],'BJ',data[1],'2023-01-16')

    return HttpResponse('执行完毕！')

@prevent_duplicate_calls
def pe_dayadd(request):
    setattr(request, 'no_cache', True)
    
    if request.method == 'GET':
      path =  os.path.dirname(__file__)
   
      filename = ""
      if(sysstr =="Windows"):
        filename = path+"\\Table1.xls"       
      else:
        filename = path+"/Table1.xls"
    
      df = pd.read_excel(filename, sheet_name='工作表1', header=0)
      df = df.drop_duplicates()
      df = df.reset_index(drop=True)
      duplicates = df.duplicated()
         
      dt='2024-08-05'
      symbol=''
      # 遍历非重复行
      for index, row in df[~duplicates].iterrows():
        if str(row.开盘).lstrip().rstrip()[0:1] != '―':
            code = str(row.代码).lstrip().rstrip()
            if len(code) == 1:
                code = '00000'+ code
            elif len(code) == 2:
                code = '0000'+ code
            elif len(code) == 3:    
                code = '000'+ code
            elif len(code) == 4:    
                code = '00'+ code
            elif len(code) == 5:    
                code = '0'+ code
            
            print('非重复行'+code)
                       
            volume = 0
            if '万' in str(row.总量):
                volume = round(float(row.总量[0:-1])*10000,2)
            else:
                volume = round(float(row.总量*1),2)
          
            amount = 0
            if '万' in (row.金额):
                amount = round(float(row.金额[0:-1]),2)
            elif '亿' in row.金额:
                amount = round(float(row.金额[0:-1])*10000,2)
            else:
                amount = round(float(row.金额*0.0001),2)
                          
            data = [code,row.换手, row.量比, row.市盈率,row.委比]  
            if symbol!=code:
                print(data)
                everyday_pe(data[0],data[1],data[2],data[3],data[4],dt)
                symbol=code
                    
             
      # 处理重复行
      for index, row in df[duplicates].iterrows():
        print('重复行'+str(row.代码))                            
                            
    return HttpResponse('执行完毕！')

@prevent_duplicate_calls
def dayadd(request):
    setattr(request, 'no_cache', True)
    
    if request.method == 'GET':
      path =  os.path.dirname(__file__)
   
      filename = ""
      if(sysstr =="Windows"):
        filename = path+"\\Table1.xls"       
      else:
        filename = path+"/Table1.xls"
    
      df = pd.read_excel(filename, sheet_name='工作表1', header=0)
      df = df.drop_duplicates()
      df = df.reset_index(drop=True)
      duplicates = df.duplicated()
         
      dt='2024-08-05'
      symbol=''
      # 遍历非重复行
      for index, row in df[~duplicates].iterrows():
        if str(row.开盘).lstrip().rstrip()[0:1] != '―':
            code = str(row.代码).lstrip().rstrip()
            if len(code) == 1:
                code = '00000'+ code
            elif len(code) == 2:
                code = '0000'+ code
            elif len(code) == 3:    
                code = '000'+ code
            elif len(code) == 4:    
                code = '00'+ code
            elif len(code) == 5:    
                code = '0'+ code
            
            print('非重复行'+code)
                       
            volume = 0
            if '万' in str(row.总量):
                volume = round(float(row.总量[0:-1])*10000,2)
            else:
                volume = round(float(row.总量*1),2)
          
            amount = 0
            if '万' in (row.金额):
                amount = round(float(row.金额[0:-1]),2)
            elif '亿' in row.金额:
                amount = round(float(row.金额[0:-1])*10000,2)
            else:
                amount = round(float(row.金额*0.0001),2)
                    
            if code[:2] == '30':  
                    try:
                        get_object_or_404(Stockszc, code=code,date=dt)
                    except Http404:
                        data = [code,row.开盘,row.最新,row.最高,row.最低,volume,amount,row.换手,row.量比,row.涨幅,row.涨跌,row.昨收,row.市盈率,row.委比]  
                        if symbol!=code:
                            print(data)
                            everyday(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],dt)
                            symbol=code
            elif code[:2] == '00':
                    try:
                        get_object_or_404(Stocksz, code=code,date=dt)
                    except Http404:
                        data = [code,row.开盘,row.最新,row.最高,row.最低,volume,amount,row.换手,row.量比,row.涨幅,row.涨跌,row.昨收,row.市盈率,row.委比]  
                        if symbol!=code:
                            print(data)
                            everyday(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],dt)
                            symbol=code
            elif code[:2] == '68':
                    try:
                        get_object_or_404(Stockshk, code=code,date=dt)   
                    except Http404:
                        data = [code,row.开盘,row.最新,row.最高,row.最低,volume,amount,row.换手,row.量比,row.涨幅,row.涨跌,row.昨收,row.市盈率,row.委比]  
                        if symbol!=code:
                            print(data)
                            everyday(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],dt)
                            symbol=code
            elif code[:2] == '60':    
                    try:
                        get_object_or_404(Stocksh, code=code,date=dt)
                    except Http404:
                        data = [code,row.开盘,row.最新,row.最高,row.最低,volume,amount,row.换手,row.量比,row.涨幅,row.涨跌,row.昨收,row.市盈率,row.委比]
                        if symbol!=code:
                            print(data)
                            everyday(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],dt)   
                            symbol=code
            else:
                    try:
                        get_object_or_404(Stockbj, code=code,date=dt)
                    except Http404:
                        data = [code,row.开盘,row.最新,row.最高,row.最低,volume,amount,row.换手,row.量比,row.涨幅,row.涨跌,row.昨收,row.市盈率,row.委比]    
                        if symbol!=code:
                            print(data)
                            everyday(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],dt)
                            symbol=code
      # 处理重复行
      for index, row in df[duplicates].iterrows():
        print('重复行'+str(row.代码))                            
                            
    return HttpResponse('执行完毕！')

@prevent_duplicate_calls
def indexadd(request):
    path =  os.path.dirname(__file__)
    filename = "" 
    if(sysstr =="Windows"):
        filename = path+"\\Table3.xls"
        
    else:
        filename = path+"/Table3.xls"
     
    df = pd.read_excel(filename, sheet_name='工作表1', header=0)  
    
    dt='2024-08-05'
    for row in df.itertuples():
        print(row.名称)
        code = str(row.代码)[-6:]
        print(code)
        if code in ['000001','000016','000300','000688','000905','399001','399006','899050','888801']: 
            volume = round(float(row.总手*1/1000000),2)
            amount = round(float(row.金额/100000000),2)
        
            everyday_index(code,row.名称, row.开盘, row.现价, row.最高, row.最低, volume, amount, row.涨跌,  row.涨幅, row.振幅, dt)
        
    return HttpResponse('执行完毕！')    

@prevent_duplicate_calls
def indexpe(request):
    path =  os.path.dirname(__file__)
    filename = "" 
    if(sysstr =="Windows"):
        filename = path+"\\指数市盈率.xls"
        
    else:
        filename = path+"/指数市盈率.xls"
        
    df = pd.read_excel(filename, sheet_name='工作表1', header=0)  
    
    dt='2024-08-05'
    for row in df.itertuples():
        code = str(row.代码)
        if len(code) == 1:
            code = '00000'+ code
        elif len(code) == 2:
            code = '0000'+ code
        elif len(code) == 3:    
            code = '000'+ code
        elif len(code) == 4:    
            code = '00'+ code
        elif len(code) == 5:    
            code = '0'+ code
                
        print(code)
        print(row.市盈率)
        
        everyday_indexpe(code,row.市盈率, dt)
            
    
    return HttpResponse('执行完毕！') 

@prevent_duplicate_calls    
def blockdayadd(request):
    path =  os.path.dirname(__file__)
    filename = "" 
    if(sysstr =="Windows"):
        filename = path+"\\板块指数.xls"
        
    else:
        filename = path+"/板块指数.xls"
        
    df = pd.read_excel(filename, sheet_name='工作表1', header=0)
    dt='2024-08-05'
    for row in df.itertuples():
        print(row.名称)
        
        open=0
        try:
            open=round(float(row.今开),2)
        except:
            continue
        
        turnover=0.01
        try:
            turnover=round(float(row.换手),2)
        except:
            pass
        
        limitup_number = 0
        
        try:
            limitup_number=round(float(row.涨停数),2)
        except:
            pass
        
        Continuerise_days=0
        
        try:
            Continuerise_days=round(float(row.连涨天),2)
        except:
            pass
        
        growth_pre = 0
        try:
            growth_pre=round(float(row.昨涨幅),2)
        except:
            pass
        
        growth_3 = 0
        try:
            growth_3 = round(float(row.th涨幅),2)
        except:
            pass
        
        growth_fall = str(row.涨跌数)
        if len(growth_fall)>=5:
            if row.涨幅 > 0 and len(growth_fall) == 5:
                if ',' not in growth_fall:  
                    growth_fall = growth_fall[:3]+','+growth_fall[-2:]
            elif row.涨幅 < 0 and len(growth_fall) == 5:
                if ',' not in growth_fall:
                    growth_fall = growth_fall[:2]+','+growth_fall[-3:]
            
            if  len(growth_fall) > 5 :
                if ',' not in growth_fall:
                    growth_fall = growth_fall[:3]+','+growth_fall[-3:]
                  
        
        Continuerise_30_limitup = 0
        try:
            Continuerise_30_limitup = Stocksector.objects.filter(code = row.代码).order_by('-date')[:30].aggregate(sum=Sum('limitup_number'))['sum']    
            Continuerise_30_limitup =  round(float(Continuerise_30_limitup),2)
        except:
            Continuerise_30_limitup = row.涨停数
        
        
            
        everyday_block(row.代码,row.名称,row.今开,row.现价,row.最高,row.最低,row.总量,turnover,row.量比,row.昨收,limitup_number,row.涨幅,growth_pre,growth_3,growth_fall,Continuerise_30_limitup,Continuerise_days,row.市盈率,dt)

    return HttpResponse('执行完毕！')

def dayout(request):
    everydayout('2023-02-08')
    return HttpResponse('执行完毕！')

@prevent_duplicate_calls
def inflow(request):
    setattr(request, 'no_cache', True)
    if request.method == 'GET':
      path =  os.path.dirname(__file__)
      filename = "" 
      if(sysstr =="Windows"):
        filename = path+"\\Table2.xls"       
      else:
        filename = path+"/Table2.xls"
        
      df = pd.read_excel(filename, sheet_name='工作表1', header=0)
      df = df.drop_duplicates()
      df = df.reset_index(drop=True)
      duplicates = df.duplicated()
    
      dt='2024-08-05'
      # 遍历非重复行
      for index, row in df[~duplicates].iterrows():
        code = str(row.代码)
        if len(code) == 1:
            code = '00000'+ code
        elif len(code) == 2:
            code = '0000'+ code
        elif len(code) == 3:    
            code = '000'+ code
        elif len(code) == 4:    
            code = '00'+ code
        elif len(code) == 5:    
            code = '0'+ code
            
        print('非重复行'+code)
        print(row.名称)
        inf = str(row.主力净流入)
    
        if '万' in inf:
            inf = round(float(inf[0:-1]),2)
        elif '亿' in inf:
            inf = round(float(inf[0:-1])*10000,2)
        else:
            try:
               inf = round(float(inf[0:-1])*0.0001,2)
            except: 
               inf = 0
            
        everyday_inflow0(code, inf, dt)
        
      # 处理重复行
      for index, row in df[duplicates].iterrows():
        print('重复行'+str(row.代码))  
    
    return HttpResponse('执行完毕！')

def nf(request):
    path =  os.path.dirname(__file__)
    filename = "" 
    if(sysstr =="Windows"):
        filename = path+"\\北向资金排名.xls"       
    else:
        filename = path+"/北向资金排名.xls"
        
    df = pd.read_excel(filename, sheet_name='Sheet1', header=0)
    
    dt='2024-12-23'
    for row in df.itertuples():
        code = str(row.代码)
        if len(code) == 1:
            code = '00000'+ code
        elif len(code) == 2:
            code = '0000'+ code
        elif len(code) == 3:    
            code = '000'+ code
        elif len(code) == 4:    
            code = '00'+ code
        elif len(code) == 5:    
            code = '0'+ code
            
        print(code)
        print(row.名称)
        inf = str(row.净流入)
    
        if '万' in inf:
            temp = inf[0:-1]
            if ',' in temp:
                newstr = temp.replace(',', '')
                inf = round(float(newstr),2)
            else:    
                inf = round(float(inf[0:-1]),2)
        elif '亿' in inf:
            inf = round(float(inf[0:-1])*10000,2)
        else:
            try:
               inf = round(float(inf[0:-1])*0.0001,2)
            except: 
               inf = 0
        print(inf)
        everyday_nf(code, inf, dt)
    
    return HttpResponse('执行完毕！')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   



def stock_pe(request):
    path =  os.path.dirname(__file__)
    filename = "" 
    if(sysstr =="Windows"):
        filename = path+"\\Table1.xls"       
    else:
        filename = path+"/Table1.xls"
        
    df = pd.read_excel(filename, sheet_name='工作表1', header=0)
    for row in df.itertuples():
        if str(row.开盘).lstrip().rstrip()[0:1] != '―':
            code = str(row.代码)
            if len(code) == 1:
                code = '00000'+ code
            elif len(code) == 2:
                code = '0000'+ code
            elif len(code) == 3:    
                code = '000'+ code
            elif len(code) == 4:    
                code = '00'+ code
            elif len(code) == 5:    
                code = '0'+ code
            
            print(code)
            print(row.市盈率)
            everyday_stockpe(code, row.市盈率, '2024-04-09')
    
    return HttpResponse('执行完毕！')

def block_pe(request):
    path =  os.path.dirname(__file__)
    filename = "" 
    if(sysstr =="Windows"):
        filename = path+"\\板块指数.xls"
        
    else:
        filename = path+"/板块指数.xls"
        
    df = pd.read_excel(filename, sheet_name='工作表1', header=0)
    for row in df.itertuples():
        print(row.名称) 
        print(row.市盈率)    
        everyday_blockpe(row.代码,row.市盈率,'2024-04-09')

    
    return HttpResponse('执行完毕！')

def indexpe_single(request):
    path =  os.path.dirname(__file__)
    filename = "" 
    if(sysstr =="Windows"):
        filename = path+"\\指数历史市盈率.xls"  
    else:
        filename = path+"/指数历史市盈率.xls"
        
    df = pd.read_excel(filename, sheet_name='Sheet1', header=0)  
    for row in df.itertuples():
        dt = str(row.时间区间)
        dt = dt[:4]+'-'+dt[4:6]+'-'+dt[6:8]
        
        print(dt)
        code = '000001'
        print(code)
        print(row.市盈率)
       
        
        
        everyday_indexpe(code, row.市盈率, dt)
        
    return HttpResponse('执行完毕！')      
    
    
def inflow_single(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code = request.POST['code']
        
            path =  os.path.dirname(__file__)
            filename = "" 
            if(sysstr =="Windows"):
                filename = path+"\\"+code+".xls"       
            else:
                filename = path+"/"+code+".xls"
        
            df = pd.read_excel(filename, sheet_name='Sheet1', header=0)
            for row in df.itertuples():            
                print(code)
                print(row.日期.strftime("%Y-%m-%d"))
                inf = str(row.主力净流入)
                print(inf)
                if '万' in inf:
                    inf = round(float(inf[0:-1]),2)
                elif '亿' in inf:
                    inf = round(float(inf[0:-1])*10000,2)
                else:
                    try:
                        inf = round(float(inf[0:-1])*0.001,2)
                    except: 
                        inf = 0
                everyday_inflow0(code, inf, row.日期.strftime("%Y-%m-%d"))
          
            return HttpResponse('执行完毕！')
    else:
        form = CodeForm()
        
        return render(request, 'inflow.html', {'form': form})

def get_file_list(path):
    file_list = []
    for file_name in  os.listdir(path):
        full_path = os.path.join(path,file_name)
        if os.path.isfile(full_path):
            file_list.append(full_path)
        elif os.path.isdir(full_path):
            file_list.extend(get_file_list(full_path))
            
    return file_list
            
    
def inflow_files(request):
    path =  os.path.dirname(__file__)
    file_path = "" 
    if(sysstr =="Windows"):
        file_path = path+"\\files"     
    else:
        file_path = path+"/files"
    
    file_list = get_file_list(file_path)
   
    for file_name in file_list:
        print(file_name)
        df = pd.read_excel(file_name, sheet_name='Sheet1', header=0)
        for row in df.itertuples():            
            print(file_name[-10:-4])
            print(row.日期.strftime("%Y-%m-%d"))
            print(row.换手率)
            inf = str(row.主力净流入)
            print(inf)
            if '万' in inf:
                inf = round(float(inf[0:-1]),2)
            elif '亿' in inf:
                inf = round(float(inf[0:-1])*10000,2)
            else:
                try:
                    inf = round(float(inf[0:-1])*0.001,2)
                except: 
                    inf = 0
            everyday_inflow(file_name[-10:-4], inf, row.日期.strftime("%Y-%m-%d"),row.换手率)
    
    return HttpResponse('执行完毕！')     
    
def stock_single(request):
    path =  os.path.dirname(__file__)
    filename = "" 
    if(sysstr =="Windows"):
        filename = path+"\\Table6.xls"       
    else:
        filename = path+"/Table6.xls"
        
    df = pd.read_excel(filename, sheet_name='工作表1', header=0)
    for row in df.itertuples():
        dt = str(row.时间[0:10])
        print(dt)
        print(row.金额)
        amount = round((row.金额)/10000,2)
        
        turnover('000548','SZ',row.换手, amount, dt)
        
    return HttpResponse('执行完毕！')

def index_single(request):
    path =  os.path.dirname(__file__)
    filename = ""
    if(sysstr =="Windows"):
        filename = path+"\\Table5.xls"       
    else:
        filename = path+"/Table5.xls"
        
    df = pd.read_excel(filename, sheet_name='工作表1', header=0)
    for row in df.itertuples():
        dt = str(row.时间[0:10])
        print(dt)
        
        volume = round(float(row.总手*1/1000000),2)
        amount = round(float(row.金额/100000000),2)
        
        everyday_index('899050','北证50', row.开盘, row.收盘, row.最高, row.最低, volume, amount, row.涨跌,  row.涨幅, row.振幅, dt)
       
    return HttpResponse('执行完毕！')

def block_single(request):
    path =  os.path.dirname(__file__)
    filename = ""
    code = "880817"
    name ="商誉减值"
    if(sysstr =="Windows"):
        filename = path+"\\"+code+".csv"       
    else:
        filename = path+"/"+code+".csv"
        
    df = pd.read_csv(filename, encoding='utf-8')
    for row in df.itertuples():
        dt = str(row.日期)
        print(dt)
        print(code)
        print(name)
        
        volume = round(float(row.成交量*1),2)
        block_history(code,name, row.开盘, row.收盘, row.最高, row.最低, volume, dt)
       
    return HttpResponse('执行完毕！')

def blockadd(request):
    path =  os.path.dirname(__file__)
    filename = "" 
    blockname ="陆股通"
    if(sysstr =="Windows"):
        filename = path+"\\"+blockname+".xls"
    else:
        filename = path+"/"+blockname+".xls"
        
    df = pd.read_excel(filename, sheet_name='工作表1', header=0)
    
    for row in df.iloc[:,0:2].itertuples():
        my = str(row.代码)
        if len(my) == 1:
            my = '00000'+ my
        elif len(my) == 2:
            my = '0000'+ my
        elif len(my) == 3:    
            my = '000'+ my
        elif len(my) == 4:    
            my = '00'+ my
        elif len(my) == 5:    
            my = '0'+ my    
        print(my)
        print(row.名称)
        board = get_object_or_404(Board,name=blockname)  
        try:
            stocks = get_object_or_404(Stocks,code=my)
            
            if  not stocks.boards.filter(name=blockname):
                stocks.boards.add(board)
                stocks.blockname = blockname
                stocks.save()
            elif stocks.boards.filter(name=blockname):
                stocks.blockname = blockname
                stocks.save()
                    
        except Http404:
            stocks = Stocks.objects.create(
                code = my,
                name = row.名称,
                blockname = blockname
            )
            stocks.boards.add(board)
            stocks.save() 

    return HttpResponse('执行完毕！')