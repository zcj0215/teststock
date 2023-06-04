from django.shortcuts import render

# Create your views here.
import os
from astocks.models import Stocksz,Stockszc,Stocksh,Stockshk,Stockbj
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
import platform
from django.db.models import Q

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
    
def turnover(code,flag,dd,dt):
    if flag == 'SZ':
        if code[:2] == '30':  
            try:
                stock = get_object_or_404(Stockszc, code=code,date=dt)
                stock.turnover = float(dd)
                stock.save()
            except Http404:
                pass
        else:
            try:
                stock = get_object_or_404(Stocksz, code=code,date=dt)
                stock.turnover = float(dd)
                stock.save()
            except Http404:
                pass
    elif flag == 'SH':
        if code[:2] == '68':  
            try:
                stock = get_object_or_404(Stockshk, code=code,date=dt)
                stock.turnover = float(dd)
                stock.save()
            except Http404:
                pass
        else:     
            try:
                stock = get_object_or_404(Stocksh, code=code,date=dt)
                stock.turnover = float(dd)
                stock.save()
            except Http404:
                pass
    elif flag == 'BJ':
            try:
                stock = get_object_or_404(Stockbj, code=code,date=dt)
                stock.turnover = float(dd)
                stock.save()
            except Http404:
                pass


def everyday(code,open,close,high,low,volume,amount,turnover,volume_ratio,p_change,price_change,pre_close,dt):
   
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
        turnover('000158','SZ',data[1], data[0])

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
        everyday(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],'2023-06-02')

    return HttpResponse('执行完毕！')

def dayout(request):
    everydayout('2023-02-08')
    return HttpResponse('执行完毕！')
