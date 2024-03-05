from django.shortcuts import render

# Create your views here.
import os
from astocks.models import Stocksz,Stockszc,Stocksh,Stockshk,Stockbj,Stocks,Stocksector,StockChoose,StockLimitup
from boards.models import Board,BoardType
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from .forms import CodeForm
import platform
from django.db.models import Q

import pandas as pd

sysstr = platform.system()

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


def everyday(code,open,close,high,low,volume,amount,turnover,volume_ratio,p_change,price_change,pre_close,dt):
    
    try:
        stock = get_object_or_404(Stocks, code=code)
        stock.growth = round(float(p_change),2)
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
                volume_ratio = round(float(volume_ratio),2)
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
                volume_ratio = round(float(volume_ratio),2)
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
                volume_ratio = round(float(volume_ratio),2)
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
                volume_ratio = round(float(volume_ratio),2)
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
                volume_ratio = round(float(volume_ratio),2)
            )
            
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
    

def everyday_block(code,name,open,close,high,low,volume,tover,volume_ratio,pre_close,limitup_number,growth,growth_pre,growth_3,growth_20,growth_60,Continuerise_days,dt):
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
        block.growth_20 = round(float(growth_20),2)
        block.growth_60 = round(float(growth_60),2)
        block.Continuerise_days = round(float(Continuerise_days),2)
        block.name = name
        block.save()
    except Http404:
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
                growth_20 = round(float(growth_20),2),
                growth_60 = round(float(growth_60),2),
                Continuerise_days = round(float(Continuerise_days),2),
                date = dt     
        )
    
    

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

def dayadd(request):
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
                data_temp[0] = data_temp[0][0:6]
                data_temp[1] = data_temp[1].lstrip().rstrip()
                data_temp[2] = data_temp[2].lstrip().rstrip()
                data_temp[3] = data_temp[3].lstrip().rstrip()
                data_temp[4] = data_temp[4].lstrip().rstrip()
                data_temp[5] = data_temp[5].lstrip().rstrip()
                data_temp[6] = data_temp[6].lstrip().rstrip()
                data_temp[7] = data_temp[7].lstrip().rstrip()
                data_temp[8] = data_temp[8].lstrip().rstrip()
                data_temp[9] = data_temp[9].lstrip().rstrip()
                data_temp[10] = data_temp[10].lstrip().rstrip()
                data_temp[11] = data_temp[11].lstrip().rstrip()

                if data_temp[6] == '':
                    data_temp[6] = data_temp[7]
                    data_temp[7] = data_temp[8]
                    data_temp[8] = data_temp[9]
                    data_temp[9] = data_temp[10]
                    data_temp[10] = data_temp[11]
                    data_temp[11] = data_temp[12].lstrip().rstrip()

                if data_temp[9] == '':
                    data_temp[9] = data_temp[10]
                    data_temp[10] = data_temp[11]
                    data_temp[11] = data_temp[12].lstrip().rstrip()

                if data_temp[8] == '—':
                    data_temp[8] = '0.01'

                data_list.append([data_temp[0],data_temp[1],data_temp[2],data_temp[3],data_temp[4],data_temp[5],data_temp[6],data_temp[7],
                          data_temp[8],data_temp[9],data_temp[10],data_temp[11]])

    for data in data_list:
      if data[1][0:1] != '—':
        if '万' in data[5]:
            data[5] = round(float(data[5][0:-1])*10000,2)
        else:
            data[5] = round(float(data[5]),2)

        if '万' in data[6] or '亿' in data[6]:
            if '万' in data[6]:
                data[6] = round(float(data[6][0:-1]),2)
            elif '亿' in data[6]:
                data[6] = round(float(data[6][0:-1])*10000,2)
        
        print(data)
        everyday(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],'2024-03-05')

    return HttpResponse('执行完毕！')


def blockadd(request):
    path =  os.path.dirname(__file__)
    filename = "" 
    if(sysstr =="Windows"):
        filename = path+"\\AI手机PC.xls"
    else:
        filename = path+"/AI手机PC.xls"
        
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
        board = get_object_or_404(Board,name='AI手机PC')  
        try:
            stocks = get_object_or_404(Stocks,code=my)
            
            if  not stocks.boards.filter(name='AI手机PC'):
                stocks.boards.add(board)
                stocks.blockname = 'AI手机PC'
                stocks.save()
            elif stocks.boards.filter(name='AI手机PC'):
                stocks.blockname = 'AI手机PC'
                stocks.save()
                    
        except Http404:
            stocks = Stocks.objects.create(
                code = my,
                name = row.名称,
                blockname = 'AI手机PC'
            )
            stocks.boards.add(board)
            stocks.save() 

    return HttpResponse('执行完毕！')


def blockdayadd(request):
    path =  os.path.dirname(__file__)
    filename = "" 
    if(sysstr =="Windows"):
        filename = path+"\\板块指数.xls"
        
    else:
        filename = path+"/板块指数.xls"
        
    df = pd.read_excel(filename, sheet_name='工作表1', header=0)
    
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
        
        growth_20 = 0
        
        try:
            growth_20 = round(float(row.tw涨幅),2)
        except:
            pass
        
        growth_60 = 0
        
        try:
            growth_60 = round(float(row.six涨幅),2)
        except:
            pass
            
        everyday_block(row.代码,row.名称,row.今开,row.现价,row.最高,row.最低,row.总量,turnover,row.量比,row.昨收,limitup_number,row.涨幅,growth_pre,growth_3,growth_20,growth_60,Continuerise_days,'2024-03-05')

    return HttpResponse('执行完毕！')

def dayout(request):
    everydayout('2023-02-08')
    return HttpResponse('执行完毕！')


def inflow(request):
    path =  os.path.dirname(__file__)
    filename = "" 
    if(sysstr =="Windows"):
        filename = path+"\\Table.xls"       
    else:
        filename = path+"/Table.xls"
        
    df = pd.read_excel(filename, sheet_name='工作表1', header=0)
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
        inf = str(row.主力净流入)
    
        if '万' in inf:
            inf = round(float(inf[0:-1]),2)
        elif '亿' in inf:
            inf = round(float(inf[0:-1])*10000,2)
        else:
            try:
               inf = round(float(inf[0:-1])*0.001,2)
            except: 
               inf = 0
            
        everyday_inflow0(code, inf, '2024-03-05')
    
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
        filename = path+"\\Table1.xls"       
    else:
        filename = path+"/Table1.xls"
        
    df = pd.read_excel(filename, sheet_name='工作表1', header=0)
    for row in df.itertuples():
        dt = str(row.时间[0:10])
        print(dt)
        print(row.金额)
        amount = round((row.金额)/10000,2)
        
        turnover('300638','SZ',row.换手, amount, dt)
        
    return HttpResponse('执行完毕！')
