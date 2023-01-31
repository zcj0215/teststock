from django.shortcuts import render

# Create your views here.
import os
from astocks.models import Stocksz,Stockszc,Stocksh,Stockshk,Stockbj
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
import platform

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
        turnover('600418','SH',data[1], data[0])

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
        everyday(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],'2023-01-30')

    return HttpResponse('执行完毕！')